from typing import Dict
import numpy as np
import torch
from torch import Tensor, nn
from probe_ably.core.models import AbstractModel 


class LinearModel(AbstractModel):

    def __init__(self, representation_size=768, n_classes=3, dropout=0.1):
        super().__init__()
        self.linear = nn.Linear(representation_size, n_classes)
        self.dropout = nn.Dropout(dropout)
        self.criterion = nn.CrossEntropyLoss()

    def forward(self, representation:Tensor, labels:Tensor, **kwargs) -> Dict[str, Tensor] :
        """forward method

        Args:
            representation (Tensor): Representation tensors
            labels (Tensor): Prediciton labels

        Returns:
            Dict[str, Tensor]: Return dictionary of {'loss': loss, 'preds': preds }
        """        
        embeddings = self.dropout(representation)
        logits = self.linear(embeddings)
        preds = logits.max(1).indices
        loss = self.criterion(logits, labels)
        return {'loss': loss, 'preds': preds}

    def get_complexity(self, **kwargs)-> Dict[str,float]:
        """Computes the complexity

        Returns:
            float: Returns the complexity value
        """
        return {"norm":self.get_norm()}

    def get_norm(self):
        ext_matrix = torch.cat([self.linear.weight, self.linear.bias.unsqueeze(-1)], dim=1)
        penalty = torch.norm(ext_matrix, p='nuc').item()
        return float(penalty)

#    def get_rank(self):
#        ext_matrix = torch.cat([self.linear.weight, self.linear.bias.unsqueeze(-1)], dim=1)
#        _, svd_matrix, _ = np.linalg.svd(ext_matrix.cpu().numpy())
#        rank = np.sum(svd_matrix > 1e-3)
#        return rank