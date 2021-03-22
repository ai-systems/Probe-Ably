from typing import Dict
import numpy as np
import torch
from torch import Tensor, nn
from probe_ably.core.models import AbstractModel


class MLPModel(AbstractModel):
    def __init__(
        self, params: Dict
    ):  # representation_size=768, n_classes=3, hidden_size=5, n_layers=1, dropout=0.1
        super().__init__()
        self.representation_size = params["representation_size"]
        self.n_layers = params["n_layers"]
        self.hidden_size = params["hidden_size"]
        if self.hidden_size < 2**self.n_layers:
            self.hidden_size = 2**self.n_layers
        self.dropout_p = params["dropout"]
        self.n_classes = params["n_classes"]

        self.mlp = self.build_mlp()
        self.linear = nn.Linear(self.final_hidden_size, self.n_classes)
        self.dropout = nn.Dropout(self.dropout_p)
        self.criterion = nn.CrossEntropyLoss()

    def forward(
        self, representation: Tensor, labels: Tensor, **kwargs
    ) -> Dict[str, Tensor]:
        """forward method

        Args:
            representation (Tensor): Representation tensors
            labels (Tensor): Prediciton labels

        Returns:
            Dict[str, Tensor]: Return dictionary of {'loss': loss, 'preds': preds }
        """
        embeddings = self.dropout(representation)
        mlp_out = self.mlp(embeddings)
        logits = self.linear(mlp_out)
        preds = logits.max(1).indices
        loss = self.criterion(logits, labels)
        return {"loss": loss, "preds": preds}

    def get_complexity(self, **kwargs) -> Dict[str, float]:
        """Computes the complexity

        Returns:
            float: Returns the complexity value
        """
        return {"nparams": self.get_n_params()}

    def build_mlp(self):
        if self.n_layers == 0:
            self.final_hidden_size = self.representation_size
            return nn.Identity()
        src_size = self.representation_size
        tgt_size = self.hidden_size
        mlp = []
        for _ in range(self.n_layers):
            mlp += [nn.Linear(src_size, tgt_size)]
            mlp += [nn.ReLU()]
            mlp += [nn.Dropout(self.dropout_p)]
            src_size, tgt_size = tgt_size, int(tgt_size / 2)
        self.final_hidden_size = src_size
        return nn.Sequential(*mlp)

    def get_n_params(self):
        pp = 0

        for p in list(self.parameters()):
            nn = 1
            for s in list(p.size()):
                nn = nn * s
            pp += nn
        return pp
