"""gnn_property_predictor.py
Graph Neural Network (GNN) property predictor using PyTorch Geometric (PyG).

This module is optional but provides higher-accuracy predictions of activation
energy / conductivity / stability than traditional ML descriptors by
operating directly on crystal graphs.

If PyG is not available, a fallback dense network is used.
"""

from __future__ import annotations

from typing import Dict, List, Optional

import torch
import torch.nn as nn

try:
    from torch_geometric.nn import CGConv, global_mean_pool  # type: ignore
    from torch_geometric.data import Data
except Exception:  # pragma: no cover
    CGConv = None  # type: ignore
    global_mean_pool = None  # type: ignore
    Data = None  # type: ignore


class CrystalGNN(nn.Module):
    """Simple crystal graph network (CGCNN-like)."""

    def __init__(self, node_dim: int = 64, hidden: int = 128, out_dim: int = 1):
        super().__init__()
        self.use_pyg = CGConv is not None
        if self.use_pyg:
            self.conv1 = CGConv(node_dim, dim=hidden)
            self.conv2 = CGConv(node_dim, dim=hidden)
            self.fc = nn.Sequential(
                nn.Linear(node_dim, hidden),
                nn.ReLU(),
                nn.Linear(hidden, out_dim),
            )
        else:
            # Fallback – dense MLP
            self.fc = nn.Sequential(
                nn.Linear(node_dim, hidden),
                nn.ReLU(),
                nn.Linear(hidden, out_dim),
            )

    def forward(self, data):  # type: ignore[override]
        if self.use_pyg and isinstance(data, Data):
            x, edge_index = data.x, data.edge_index
            x = self.conv1(x, edge_index)
            x = self.conv2(x, edge_index)
            x = global_mean_pool(x, data.batch)
            return self.fc(x)
        else:
            return self.fc(data)  # type: ignore[arg-type]


class GNNPropertyPredictor:
    """High-level wrapper to train & predict with CrystalGNN on materials dataset."""

    def __init__(self, target: str = "conductivity"):
        self.target = target
        self.model: Optional[nn.Module] = None
        self.scaler_mean: float = 0
        self.scaler_std: float = 1

    def train(self, dataset, epochs: int = 50, lr: float = 1e-3):
        """Train on provided PyG InMemoryDataset or fallback tensors."""
        if CGConv is None:
            # Expect dataset as (X, y) tensors
            X, y = dataset
            self.model = CrystalGNN(node_dim=X.shape[1])
            optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
            loss_fn = nn.MSELoss()
            for _ in range(epochs):
                optimizer.zero_grad()
                pred = self.model(X)
                loss = loss_fn(pred, y)
                loss.backward()
                optimizer.step()
        else:
            loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)
            self.model = CrystalGNN()
            optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
            loss_fn = nn.MSELoss()
            self.model.train()
            for _ in range(epochs):
                for batch in loader:
                    batch = batch.to("cpu")
                    optimizer.zero_grad()
                    pred = self.model(batch)
                    loss = loss_fn(pred.squeeze(), batch.y)
                    loss.backward()
                    optimizer.step()

    def predict(self, data):
        if self.model is None:
            raise RuntimeError("Model not trained or loaded.")
        self.model.eval()
        with torch.no_grad():
            return self.model(data) 