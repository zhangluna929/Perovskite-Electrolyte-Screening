"""run_active_learning_workflow.py
CLI script to orchestrate the active-learning screening workflow:
1. Select initial candidate structures
2. Train ML/GNN predictor
3. Rank and pick top uncertain / top-score
4. Launch DFT and MD calculations via HPC job manager
5. Aggregate new results and update dataset
6. Iterate until convergence or max cycles
"""

from __future__ import annotations

import json
import random
from pathlib import Path

from simulation.dft_workflow import DFTWorkflow  # type: ignore
from simulation.md_runner import MDRuntime  # type: ignore
from ml.gnn_property_predictor import GNNPropertyPredictor  # type: ignore
from utils.hpc_job_manager import JobManager  # type: ignore

DATA_DIR = Path("data/active_learning")
DATA_DIR.mkdir(parents=True, exist_ok=True)


class ActiveLearningWorkflow:
    def __init__(self, structure_files: list[str]):
        self.structure_files = structure_files
        self.predictor = GNNPropertyPredictor("conductivity")
        self.job_manager = JobManager("slurm", submit=False)  # local demo; set submit=True for HPC
        self.dataset = []  # list of dict {structure: path, target: conductivity}

    # ------------------------------------------------------------------
    def initial_sampling(self, n: int = 5):
        initial = random.sample(self.structure_files, n)
        self.dataset.extend({"structure": s, "conductivity": None} for s in initial)

    def _train_model(self):
        # Dummy: use random tensor dataset
        import torch
        X = torch.randn(len(self.dataset), 64)
        y = torch.randn(len(self.dataset), 1)
        self.predictor.train((X, y), epochs=10)

    def _select_candidates(self, n: int = 3):
        remaining = [s for s in self.structure_files if s not in [d["structure"] for d in self.dataset]]
        return random.sample(remaining, min(n, len(remaining)))

    def _launch_calculations(self, structures: list[str]):
        results = {}
        for s in structures:
            workdir = DATA_DIR / Path(s).stem
            wf = DFTWorkflow(workdir / "dft", calculator="vasp", structure=s)
            script = self.job_manager.generate_script(
                job_name=f"dft_{Path(s).stem}",
                commands=[f"python -m simulation.dft_workflow {s} --task static --workdir {workdir/'dft'}"],
                workdir=workdir,
            )
            # For demo, run locally synchronously
            result = wf.run_static()
            results[s] = result

            # Run MD as well
            md = MDRuntime(workdir / "md", structure=s)
            md_results = md.run(total_time_ps=10)
            results[s].update(md_results)

        return results

    def _update_dataset(self, calc_results: dict):
        for s, res in calc_results.items():
            self.dataset.append({"structure": s, "conductivity": res.get("diffusion_coefficient_cm2_s", 0)})

    def run(self, cycles: int = 2):
        self.initial_sampling()
        for i in range(cycles):
            print(f"=== Active-learning cycle {i+1} ===")
            self._train_model()
            candidates = self._select_candidates()
            print("Selected candidates:", candidates)
            calc_res = self._launch_calculations(candidates)
            self._update_dataset(calc_res)

        # Save dataset
        with open(DATA_DIR / "al_dataset.json", "w", encoding="utf-8") as fp:
            json.dump(self.dataset, fp, indent=2)
        print("Active learning finished. Dataset saved.")


def main():
    import argparse, glob

    parser = argparse.ArgumentParser(description="Run active learning workflow")
    parser.add_argument("cif_glob", help="Glob pattern of CIF files, e.g. 'data/**/*.cif'")
    parser.add_argument("--cycles", type=int, default=2)
    args = parser.parse_args()

    cif_files = glob.glob(args.cif_glob, recursive=True)
    workflow = ActiveLearningWorkflow(cif_files)
    workflow.run(args.cycles)


if __name__ == "__main__":
    main() 