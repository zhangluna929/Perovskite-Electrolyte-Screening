"""md_runner.py
Automated Molecular Dynamics (MD) runner wrapping LAMMPS (via ASE) or OpenMM
for the Perovskite Electrolyte Screening Platform.

The module prepares input structures (from CIF/XYZ) or `ase.Atoms` objects,
launches MD simulations, monitors progress, parses key results (temperature,
pressure, mean-square-displacement, diffusion coefficients), and exports them
as JSON for downstream screening.

Author: LunaZhang (2024)
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Union

import numpy as np
from ase import Atoms
from ase.io import read, write
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase import units
from ase.calculators.calculator import Calculator

# Optional: LAMMPS calculator
try:
    from ase.calculators.lammpsrun import LAMMPS
except Exception:  # pragma: no cover
    LAMMPS = None  # type: ignore

# Optional: OpenMM via ase-openmm
try:
    from ase.calculators.openmm import OpenMM
except Exception:  # pragma: no cover
    OpenMM = None  # type: ignore


def _build_calculator(engine: str, parameters: Dict) -> Calculator:
    """Factory returning an ASE MD-compatible calculator."""
    engine = engine.lower()
    if engine == "lammps":
        if LAMMPS is None:
            raise ImportError("LAMMPS calculator not available – install lammps and ase-lammps")
        return LAMMPS(parameters=parameters.get("lammps_params", {}))
    elif engine == "openmm":
        if OpenMM is None:
            raise ImportError("OpenMM calculator not available – install openmm and ase-openmm")
        return OpenMM(**parameters.get("openmm_params", {}))  # type: ignore[arg-type]
    else:
        raise ValueError(f"Unsupported MD engine: {engine}")


class MDRuntime:
    """High-level MD automation helper."""

    def __init__(
        self,
        workdir: Union[str, Path],
        engine: str = "lammps",
        engine_parameters: Optional[Dict] = None,
        structure: Union[str, Path, Atoms] | None = None,
    ) -> None:
        self.workdir = Path(workdir).expanduser().resolve()
        self.workdir.mkdir(parents=True, exist_ok=True)

        self.engine = engine
        self.engine_parameters = engine_parameters or {}
        self.atoms: Optional[Atoms] = None
        if structure is not None:
            self.load_structure(structure)

        self.calc: Optional[Calculator] = None
        self.results: Dict[str, float | list] = {}

    # ------------------------------------------------------------------
    # Structure handling
    # ------------------------------------------------------------------
    def load_structure(self, source: str | Path | Atoms):
        if isinstance(source, Atoms):
            self.atoms = source.copy()
        else:
            self.atoms = read(Path(source).as_posix())

    # ------------------------------------------------------------------
    # Run
    # ------------------------------------------------------------------
    def run(self, temperature: float = 300, total_time_ps: float = 100, time_step_fs: float = 1.0):
        """Run MD simulation and compute diffusion coefficient."""
        if self.atoms is None:
            raise RuntimeError("No structure loaded.")

        # Build calculator
        self.calc = self.calc or _build_calculator(self.engine, self.engine_parameters)
        self.atoms.calc = self.calc  # type: ignore[attr-defined]

        # Set initial velocities
        MaxwellBoltzmannDistribution(self.atoms, temperature_K=temperature)

        # Configure MD
        dt = time_step_fs * units.fs
        n_steps = int((total_time_ps * 1000) / time_step_fs)  # ps to fs to steps
        dyn = VelocityVerlet(self.atoms, dt, logfile=self.workdir / "md.log")

        positions = np.empty((n_steps // 10 + 1, len(self.atoms), 3))  # save every 10 steps
        times = []

        def store_positions():
            i = len(times)
            positions[i] = self.atoms.get_positions()
            times.append(dyn.get_time() / units.fs)

        dyn.attach(store_positions, interval=10)  # every 10 steps

        dyn.run(n_steps)

        positions = positions[: len(times)]  # trim unused
        msd = self._mean_square_displacement(positions)
        times_arr = np.array(times) * 1e-3  # fs → ps
        # linear fit for diffusion coefficient (d<r^2>/dt)/6
        coeff = np.polyfit(times_arr, msd, 1)[0] / 6

        self.results = {
            "temperature_K": temperature,
            "total_time_ps": total_time_ps,
            "time_step_fs": time_step_fs,
            "diffusion_coefficient_cm2_s": float(coeff * 1e-4),  # Å^2/ps to cm^2/s
            "msd": msd.tolist(),
            "times_ps": times_arr.tolist(),
        }
        self._save_results()
        return self.results

    # ------------------------------------------------------------------
    def _mean_square_displacement(self, pos: np.ndarray) -> np.ndarray:
        """Compute MSD over trajectory positions."""
        dr = pos - pos[0]
        msd = np.mean(np.sum(dr**2, axis=2), axis=1)
        return msd

    def _save_results(self):
        with open(self.workdir / "md_results.json", "w", encoding="utf-8") as fp:
            json.dump({"timestamp": datetime.now().isoformat(), **self.results}, fp, indent=2)

    # ------------------------------------------------------------------
    # CLI Interface
    # ------------------------------------------------------------------
    @staticmethod
    def from_cli():
        import argparse

        parser = argparse.ArgumentParser(description="Run MD simulation for perovskite electrolytes")
        parser.add_argument("structure", help="Path to structure file (cif, xyz, POSCAR, …)")
        parser.add_argument("--engine", choices=["lammps", "openmm"], default="lammps")
        parser.add_argument("--workdir", default="md_work")
        parser.add_argument("--temp", type=float, default=300, help="Temperature in K")
        parser.add_argument("--time", type=float, default=100, help="Total time in ps")
        parser.add_argument("--dt", type=float, default=1.0, help="Time step in fs")
        args = parser.parse_args()

        runner = MDRuntime(args.workdir, args.engine, structure=args.structure)
        runner.run(args.temp, args.time, args.dt)
        return runner


if __name__ == "__main__":
    MDRuntime.from_cli() 