"""hpc_job_manager.py
Utility to generate and submit job scripts to HPC schedulers (SLURM, PBS).

Usage example:
    from utils.hpc_job_manager import JobManager
    jm = JobManager("slurm")
    script_path = jm.generate_script(
        job_name="dft",
        commands=["python src/simulation/dft_workflow.py BaTiO3.cif --task static"],
        nodes=1, ntasks_per_node=24, time="02:00:00"
    )
    jm.submit(script_path)
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import List, Dict, Optional


class JobManager:
    def __init__(self, scheduler: str = "slurm", submit: bool = True):
        self.scheduler = scheduler.lower()
        if self.scheduler not in {"slurm", "pbs"}:
            raise ValueError("Scheduler must be 'slurm' or 'pbs'")
        self.auto_submit = submit

    # ------------------------------------------------------------------
    def generate_script(
        self,
        job_name: str,
        commands: List[str],
        workdir: str | Path = ".",
        nodes: int = 1,
        ntasks_per_node: int = 24,
        time: str = "01:00:00",
        queue: Optional[str] = None,
        modules: Optional[List[str]] = None,
    ) -> Path:
        """Write job script file and return its path."""
        workdir = Path(workdir)
        script_path = workdir / f"{job_name}.{self.scheduler}.sh"
        modules_lines = [f"module load {m}" for m in (modules or [])]
        cmd_lines = commands

        if self.scheduler == "slurm":
            header = [
                f"#!/bin/bash",
                f"#SBATCH --job-name={job_name}",
                f"#SBATCH --nodes={nodes}",
                f"#SBATCH --ntasks-per-node={ntasks_per_node}",
                f"#SBATCH --time={time}",
            ]
            if queue:
                header.append(f"#SBATCH -p {queue}")
            content = header + modules_lines + ["cd $SLURM_SUBMIT_DIR"] + cmd_lines
        else:  # PBS
            header = [
                f"#!/bin/bash",
                f"#PBS -N {job_name}",
                f"#PBS -l nodes={nodes}:ppn={ntasks_per_node}",
                f"#PBS -l walltime={time}",
            ]
            if queue:
                header.append(f"#PBS -q {queue}")
            content = header + modules_lines + ["cd $PBS_O_WORKDIR"] + cmd_lines

        script_path.write_text("\n".join(content))
        return script_path

    # ------------------------------------------------------------------
    def submit(self, script_path: Path):
        if not self.auto_submit:
            print(f"Skipped submission, auto_submit=False. Script at {script_path}")
            return
        if self.scheduler == "slurm":
            subprocess.run(["sbatch", str(script_path)], check=False)
        else:
            subprocess.run(["qsub", str(script_path)], check=False)
        print(f"Submitted job script {script_path}") 