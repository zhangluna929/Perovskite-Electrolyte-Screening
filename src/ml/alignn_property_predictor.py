"""alignn_property_predictor.py
ALIGNN (Atomistic Line Graph Neural Network) property predictor
utilising pre-trained checkpoints from JARVIS-Tools.

Supports quick inference by loading checkpoints distributed with
`jarvis-tools` and `alignn` libraries.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Union

from pymatgen.core import Structure

try:
    from jarvis.db.jsonutils import loadjson  # type: ignore
    from jarvis.models.alignn import ALIGNNConfig, ALIGNN  # type: ignore
except ImportError as exc:  # pragma: no cover
    raise ImportError("jarvis-tools & alignn packages required: pip install jarvis-tools alignn") from exc


_DEFAULT_CHECKPOINTS = {
    "formation_energy": "https://figshare.com/ndownloader/files/31954032",  # example URL
}


def _download_checkpoint(url: str, dst: Path):
    import urllib.request, shutil
    if not dst.exists():
        with urllib.request.urlopen(url) as resp, open(dst, "wb") as out:
            shutil.copyfileobj(resp, out)
    return dst


class ALIGNNPropertyPredictor:
    def __init__(self, property_name: str = "formation_energy"):
        self.property_name = property_name
        ckpt_dir = Path("models/alignn")
        ckpt_dir.mkdir(parents=True, exist_ok=True)
        ckpt_path = ckpt_dir / f"{property_name}.pt"
        url = _DEFAULT_CHECKPOINTS.get(property_name)
        if url:
            _download_checkpoint(url, ckpt_path)
        cfg = ALIGNNConfig(name="alignn", target=self.property_name, num_targets=1)
        self.model = ALIGNN(cfg)
        self.model.load_state_dict(torch.load(ckpt_path, map_location="cpu"))  # type: ignore
        self.model.eval()

    def predict_structure(self, structure: Union[str, Path, Structure]):
        if not isinstance(structure, Structure):
            structure = Structure.from_file(structure)
        # convert to atoms for alignn
        from jarvis.core.atoms import Atoms  # type: ignore
        atoms = Atoms.from_pymatgen(structure)
        data = atoms.get_graph()
        import torch
        with torch.no_grad():
            pred = self.model([data])
        return float(pred.squeeze())

    def batch_predict(self, cif_files: List[Union[str, Path]]):
        preds: Dict[str, float] = {}
        for f in cif_files:
            preds[str(Path(f).name)] = self.predict_structure(f)
        return preds 