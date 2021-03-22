from abc import ABC, abstractmethod


class AbstractIntraModelMetric(ABC):
    @abstractmethod
    def calcuate_metrics(self, targets, predicitons, **kwargs):
        ...

