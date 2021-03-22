from abc import ABC, abstractmethod


class AbstractInterModelMetric(ABC):
    @abstractmethod
    def calcuate_metrics(self, targets1, targets2, predicitons1, predicitons2, **kwargs):
        ...

