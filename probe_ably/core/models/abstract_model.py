from abc import ABC, abstractmethod
from typing import Dict

from torch import Tensor
from torch.nn import Module


class AbstractModel(Module,ABC):

    subclasses = {}
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        name = cls.__module__+'.'+cls.__qualname__
        if name in cls.subclasses:
            message = "Cannot register module %s as %s; name already in use" % (
                cls.__module__, cls.__module__)
            raise Exception(message)
        cls.subclasses[name] = cls

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
    def get_complexity(self, **kwargs)-> Dict[str,float]:
        """Computes the complexity

        Returns:
            Dict[str,float]: Returns dictionary of {"complexity_measure1": value1, "complexity_measure2": value2}
        """
        ...


