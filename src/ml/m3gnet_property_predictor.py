"""m3gnet_property_predictor.py
M3GNet (Materials graph with three-body interactions) predictor wrapper.
Provides crystal property predictions via the `m3gnet` package pre-trained
IS2RE/energy/stress/forces models and allows transfer learning on custom
datasets.

Example
-------
>>> from ml.m3gnet_property_predictor import M3GNetPropertyPredictor
>>> predictor = M3GNetPropertyPredictor("energy")
>>> e_form = predictor.predict_structure("BaTiO3.cif")
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Union

import numpy as np
from pymatgen.core import Structure

try:
    from m3gnet.models import M3GNet  # type: ignore
except ImportError as exc:  # pragma: no cover
    raise ImportError("m3gnet package required: pip install m3gnet") from exc


class M3GNetPropertyPredictor:
    """Wrapper around official M3GNet model."""

    def __init__(self, task: str = "energy", pretrained: bool = True):
        """task: one of ['energy', 'forces', 'stress', 'eos']"""
        if pretrained:
            self.model = M3GNet.from_pretrained(task)
        else:
            # Build new model architecture
            self.model = M3GNet()  # use default settings
        self.task = task

    # ------------------------------------------------------------------
    def predict_structure(self, structure: Union[str, Path, Structure]):
        if not isinstance(structure, Structure):
            structure = Structure.from_file(structure)
        result = self.model.predict_structure(structure)
        # result is dict with keys depending on task
        return result

    def batch_predict(self, cif_files: List[Union[str, Path]]):
        preds: Dict[str, Dict] = {}
        for f in cif_files:
            preds[str(Path(f).name)] = self.predict_structure(f)
        return preds

    # ------------------------------------------------------------------
    def finetune(self, *args, **kwargs):  # pragma: no cover
        """Placeholder: use official M3GNet `fit` for transfer learning."""
        raise NotImplementedError("Fine-tuning requires dataset & trainer, use model.fit().") 