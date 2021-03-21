from abc import ABC, abstractmethod


class AbstractMetric(ABC):
    @abstractmethod
    def calcuate_metrics(self, aux_gold, control_gold, aux_predicitons, control_prediciton, loss, **kwargs):
        ...

