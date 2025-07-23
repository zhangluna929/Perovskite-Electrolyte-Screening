"""megnet_property_predictor.py
MEGNet-based property predictor leveraging the materials graph network
implemented in the `megnet` package. Provides:
• out-of-the-box access to pre-trained formation-energy & band-gap models
  (shipped with MEGNet)
• easy fine-tuning / transfer learning on custom targets such as ionic
  conductivity or activation energy using Matbench or user-provided CSV.

Example
-------
>>> predictor = MEGNetPropertyPredictor("band_gap")
>>> eg = predictor.predict_structure("BaTiO3.cif")

Fine-tune on Matbench formation energy:
>>> predictor.finetune_from_matbench("matbench_logGVRH")
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, Union

import numpy as np
from pymatgen.core import Structure

try:
    from megnet.models import Model as MEGNetModel  # type: ignore
    from megnet.data.crystal import CrystalGraph
except ImportError as exc:  # pragma: no cover
    raise ImportError("megnet package required: pip install megnet") from exc


_PRETRAINED_MODELS = {
    "formation_energy": "materials_2019.4.4",
    "band_gap": "materials_2019.4.4",
}


class MEGNetPropertyPredictor:
    """Wrapper around MEGNet models with transfer-learning utilities."""

    def __init__(self, property_name: str = "formation_energy", pretrained: bool = True):
        self.property_name = property_name
        if pretrained and property_name in _PRETRAINED_MODELS:
            self.model = MEGNetModel.from_file(_PRETRAINED_MODELS[property_name] + f"_{property_name}.hdf5")
        else:
            # build new model architecture with default hyper-parameters
            self.model = MEGNetModel(
                3,  # nfeat_edge
                2,  # nfeat_global
                ntarget=1,
                graph_converter=CrystalGraph(cutoff=4.0),
            )
        self.graph_converter: CrystalGraph = self.model.graph_converter  # type: ignore[attr-defined]

    # ------------------------------------------------------------------
    # Inference helpers
    # ------------------------------------------------------------------
    def _structure_to_graph(self, structure: Structure):
        return self.graph_converter.convert(structure)

    def predict_structure(self, structure: Union[str, Path, Structure]):
        if not isinstance(structure, Structure):
            structure = Structure.from_file(structure)
        graph = self._structure_to_graph(structure)
        pred = float(self.model.predict_graph(graph)[0].squeeze())
        return pred

    def batch_predict(self, cif_files: List[Union[str, Path]]):
        structs = [Structure.from_file(f) for f in cif_files]
        graphs = [self._structure_to_graph(s) for s in structs]
        preds = self.model.predict_graphs(graphs).ravel().tolist()
        return dict(zip([str(Path(f).name) for f in cif_files], preds))

    # ------------------------------------------------------------------
    # Training / fine-tuning utilities
    # ------------------------------------------------------------------
    def finetune(
        self,
        structures: List[Structure],
        targets: np.ndarray,
        epochs: int = 100,
        lr: float = 1e-3,
        save_path: Optional[Path] = None,
    ):
        """Fine-tune the model on (structure, target) pairs."""
        graphs = [self._structure_to_graph(s) for s in structures]
        self.model.train(
            graphs,
            targets.reshape(-1, 1),
            epochs=epochs,
            lr=lr,
            batch_size=32,
            verbose=2,
        )
        if save_path:
            self.model.save(str(save_path))

    def finetune_from_matbench(self, dataset_name: str = "matbench_logGVRH", **kwargs):
        """Example: fine-tune on a Matbench dataset (requires `matbench`)."""
        try:
            from matbench.task import MatbenchTask  # type: ignore
        except ImportError as exc:  # pragma: no cover
            raise ImportError("matbench required: pip install matbench") from exc

        tb = MatbenchTask(dataset_name, subset="dev")
        tb.load()
        structures = [Structure.from_dict(d) for d in tb.data["structure"]]
        targets = tb.data[tb.target_property].values
        self.finetune(structures, np.array(targets), **kwargs)

    # ------------------------------------------------------------------
    # Export results
    # ------------------------------------------------------------------
    def save_predictions(self, preds: Dict[str, float], out_file: Union[str, Path]):
        Path(out_file).write_text(json.dumps(preds, indent=2)) 