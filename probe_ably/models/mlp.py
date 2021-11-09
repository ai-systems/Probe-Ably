## ADAPTED FROM https://github.com/rycolab/pareto-probing/blob/master/src/h02_learn/model/mlp.py
from typing import Dict

import numpy as np
import torch
from probe_ably.models import AbstractModel
from torch import Tensor, nn


class MLPModel(AbstractModel):
    def __init__(
        self, params: Dict
    ):  # representation_size=768, n_classes=3, hidden_size=5, n_layers=1, dropout=0.1
        """Initiate the MLP Model

        Args:
            params (Dict): Contains the parameters for initialization. Params data format is

                .. code-block:: json

                    {
                        'representation_size': Dimension of the representation,
                        'dropout': Dropout of module,
                        'hidden_size': Hidden layer size of MLP,
                        'n_layers': Number of MLP Layers,
                        'n_classes': Number of classes for classification,
                    }
        """
        super().__init__(params)
        self.n_layers = params["n_layers"]
        self.hidden_size = params["hidden_size"]
        # if self.hidden_size < 2 ** self.n_layers:
        #     self.hidden_size = 2 ** self.n_layers
        self.dropout_p = params["dropout"]

        self.mlp = self.build_mlp()
        self.linear = nn.Linear(self.final_hidden_size, self.n_classes)
        self.dropout = nn.Dropout(self.dropout_p)
        self.criterion = nn.CrossEntropyLoss()

    def forward(
        self, representation: Tensor, labels: Tensor, **kwargs
    ) -> Dict[str, Tensor]:
        """Forward method

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
        """Computes the number of params complexity

        Returns:
            float: Returns the complexity value of as {'n_params': number of parameters in model}
        """
        return {"hidden_size": float(self.hidden_size), "nparams": self.get_n_params()}

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
        return sum(p.numel() for p in self.parameters())

        # pp = 0

        # for p in list(self.parameters()):
        #     nn = 1
        #     for s in list(p.size()):
        #         nn = nn * s
        #     pp += nn
        # return pp
