from abc import ABC, abstractmethod
from typing import Dict

from torch import Tensor
from torch.nn import Module


class AbstractModel(Module,ABC):

    @abstractmethod
    def forward(self, representation:Tensor, labels:Tensor, **kwargs) -> Dict[str, Tensor] :
        """Abstract class forward method

        Args:
            representation (Tensor): Representation tensors
            labels (Tensor): Prediciton labels

        Returns:
            Dict[str, Tensor]: Return dictionary of {'loss': losss, 'preds': preds }
        """        
        ...

    @abstractmethod
    def get_complexity(self, **kwargs)-> float:
        """Computes the complexity

        Returns:
            float: Returns the complexity value
        """
        ...


