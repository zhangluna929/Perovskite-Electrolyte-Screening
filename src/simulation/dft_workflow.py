"""dft_workflow.py
A generic Density Functional Theory (DFT) workflow module for the Perovskite Electrolyte Screening Platform.
It provides a high-level Python API to prepare, run, and post-process quantum calculations using
ASE calculators (VASP, Quantum ESPRESSO, …) on a local machine or HPC cluster.

Author: LunaZhang (2024)
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Union

import numpy as np
from ase import Atoms
from ase.build import bulk
from ase.calculators.calculator import Calculator, all_changes
from ase.io import read, write
from ase.optimize import BFGS

# Optional imports – handled gracefully if backend not installed
try:
    from ase.calculators.vasp import Vasp  # type: ignore
except Exception:  # pragma: no cover
    Vasp = None  # type: ignore

try:
    from ase.calculators.espresso import Espresso  # type: ignore
except Exception:  # pragma: no cover
    Espresso = None  # type: ignore


class DFTWorkflow:
    """High-level driver for static/relax/band-structure DFT calculations.

    Parameters
    ----------
    workdir : str | Path
        Working directory for the calculation. Will be created if necessary.
    calculator : str {"vasp", "qe"}
        Backend code to use. Requires corresponding ASE calculator.
    calc_parameters : dict, optional
        Extra kwargs forwarded to ASE calculator constructor (encut, kpts, xc, …).
    structure : ase.Atoms | Path | str, optional
        Atomic structure to use. CIF/POSCAR/XYZ path or ase.Atoms object.
    """

    def __init__(
        self,
        workdir: Union[str, Path],
        calculator: str = "vasp",
        calc_parameters: Optional[Dict] = None,
        structure: Union[None, str, Path, Atoms] = None,
    ) -> None:
        self.workdir = Path(workdir).expanduser().resolve()
        self.workdir.mkdir(parents=True, exist_ok=True)
        self.calculator_name = calculator.lower()
        self.calc_parameters = calc_parameters or {}
        self.atoms: Optional[Atoms] = None

        if structure is not None:
            self.load_structure(structure)

        self.calc: Optional[Calculator] = None
        self.results: Dict[str, float] = {}

    # ---------------------------------------------------------------------
    # Structure utilities
    # ---------------------------------------------------------------------
    def load_structure(self, source: Union[str, Path, Atoms]) -> None:
        """Load structure into workflow."""
        if isinstance(source, Atoms):
            self.atoms = source.copy()
        else:
            source_path = Path(source)
            self.atoms = read(source_path.as_posix())

    def set_perovskite_abox(self, formula: str = "BaTiO3", a: float = 4.0) -> None:
        """Convenience method – quickly build cubic perovskite structure."""
        self.atoms = bulk(formula, "cubic", a=a)

    # ---------------------------------------------------------------------
    # Calculator factory
    # ---------------------------------------------------------------------
    def _build_calculator(self) -> Calculator:
        """Create and return an ASE calculator instance."""
        if self.calculator_name == "vasp":
            if Vasp is None:
                raise ImportError("ASE Vasp calculator not available – install ase-vasp interfaces")
            return Vasp(directory=self.workdir.as_posix(), **self.calc_parameters)
        elif self.calculator_name in {"qe", "espresso"}:
            if Espresso is None:
                raise ImportError("ASE Espresso calculator not available – install Quantum ESPRESSO support")
            return Espresso(directory=self.workdir.as_posix(), **self.calc_parameters)
        else:
            raise ValueError(f"Unsupported calculator: {self.calculator_name}")

    # ---------------------------------------------------------------------
    # Core run methods
    # ---------------------------------------------------------------------
    def run_static(self) -> Dict[str, float]:
        """Single-point energy calculation."""
        self._prepare()
        dyn = self.atoms  # type: ignore[arg-type]
        dyn.calc = self.calc  # type: ignore[attr-defined]
        energy = dyn.get_potential_energy()
        forces = dyn.get_forces()
        self.results = {
            "energy": float(energy),
            "max_force": float(np.abs(forces).max()),
        }
        self._save_results("static_results.json")
        return self.results

    def run_relax(self, fmax: float = 0.05, steps: int = 200) -> Dict[str, float]:
        """Lattice & atomic relaxation."""
        self._prepare()
        self.atoms.calc = self.calc  # type: ignore[attr-defined]
        opt = BFGS(self.atoms, trajectory=str(self.workdir / "relax.traj"), logfile=str(self.workdir / "relax.log"))
        opt.run(fmax=fmax, steps=steps)
        self.results = {
            "energy": float(self.atoms.get_potential_energy()),
            "max_force": float(np.abs(self.atoms.get_forces()).max()),
            "converged": opt.converged,
            "steps": opt.nsteps,
        }
        # Save final structure
        write(self.workdir / "relaxed_final.cif", self.atoms)
        self._save_results("relax_results.json")
        return self.results

    # ---------------------------------------------------------------------
    # Helper functions
    # ---------------------------------------------------------------------
    def _prepare(self) -> None:
        """Common preparation routine – build calculator and copy input files."""
        if self.atoms is None:
            raise RuntimeError("No structure loaded. Use load_structure() first.")
        if self.calc is None:
            self.calc = self._build_calculator()

        # In case of restart, ensure clean directory for new calculation
        for fname in ["static_results.json", "relax_results.json"]:
            (self.workdir / fname).unlink(missing_ok=True)

    def _save_results(self, filename: str) -> None:
        out_path = self.workdir / filename
        with open(out_path, "w", encoding="utf-8") as fp:
            json.dump({"timestamp": datetime.now().isoformat(), **self.results}, fp, indent=2)

    # ---------------------------------------------------------------------
    # Convenience CLI interface
    # ---------------------------------------------------------------------
    @staticmethod
    def from_cli() -> "DFTWorkflow":
        """Build workflow from command-line arguments when running as a script."""
        import argparse

        parser = argparse.ArgumentParser(description="Run a quick DFT calculation via ASE")
        parser.add_argument("structure", help="Path to structure file (cif, xyz, POSCAR, …)")
        parser.add_argument("--calc", choices=["vasp", "qe"], default="vasp", help="Backend calculator")
        parser.add_argument("--workdir", default="dft_work", help="Working directory")
        parser.add_argument("--task", choices=["static", "relax"], default="static", help="Task type")
        parser.add_argument("--encut", type=int, default=520, help="Energy cutoff (eV) – VASP/QE")
        parser.add_argument("--kpts", type=int, nargs=3, default=[6, 6, 6], help="K-point grid")
        args = parser.parse_args()

        calc_kwargs: Dict[str, Union[int, str, list]] = {
            "encut": args.encut,
            "kpts": args.kpts,
            "xc": "PBE",
        }

        wf = DFTWorkflow(args.workdir, args.calc, calc_kwargs, args.structure)
        if args.task == "static":
            wf.run_static()
        else:
            wf.run_relax()
        return wf


if __name__ == "__main__":
    # Execute from command line
    DFTWorkflow.from_cli() 