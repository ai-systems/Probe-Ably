from typing import Dict

import numpy as np
import torch
from probe_ably.core.models import AbstractModel
from torch import Tensor, nn


class LinearModel(AbstractModel):
    def __init__(self, params: Dict):
        """Initiate the Linear Model

        Args:
            params (Dict): Contains the parameters for initialization. Params data format is

                .. code-block:: json

                    {
                        'representation_size': Dimension of the representation,
                        'dropout': Dropout of module,
                        'n_classes': Number of classes for classification,
                        'alpha': Alpha value to calculate the complexity of the module
                    }
        """
        super(params).__init__()
        self.dropout_p = params["dropout"]
        self.alpha = params["alpha"]

        self.linear = nn.Linear(self.representation_size, self.n_classes)
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
        logits = self.linear(embeddings)
        preds = logits.max(1).indices
        loss = self.criterion(logits, labels) + self.alpha * self.get_norm()
        return {"loss": loss, "preds": preds}

    def get_complexity(self, **kwargs) -> Dict[str, float]:
        """Computes the Nuclear Norm complexity

        Returns:
            Dict[str, float]: Returns the complexity value of {'norm': nuclear norm score of model}
        """
        return {"norm": self.get_norm()}

    def get_norm(self) -> float:
        ext_matrix = torch.cat(
            [self.linear.weight, self.linear.bias.unsqueeze(-1)], dim=1
        )
        penalty = torch.norm(ext_matrix, p="nuc").item()
        return float(penalty)


#    def get_rank(self):
#        ext_matrix = torch.cat([self.linear.weight, self.linear.bias.unsqueeze(-1)], dim=1)
#        _, svd_matrix, _ = np.linalg.svd(ext_matrix.cpu().numpy())
#        rank = np.sum(svd_matrix > 1e-3)
#        return rank
