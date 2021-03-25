from abc import ABC, abstractmethod

import numpy as np


class AbstractIntraModelMetric(ABC):

    subclasses = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        name = cls.__module__ + "." + cls.__qualname__
        if name in cls.subclasses:
            message = "Cannot register module %s as %s; name already in use" % (
                cls.__module__,
                cls.__module__,
            )
            raise Exception(message)
        cls.subclasses[name] = cls

    @abstractmethod
    def calculate_metrics(self, targets: np.array, predicitons: np.array, **kwargs):
        """Abstract method that calcuate the intra model metric

        Args:
            targets (np.array): Gold labels of data
            predicitons (np.array): Predictions  of data

        Returns:
            float: Intra model metric score
        """
        ...

    @abstractmethod
    def metric_name(self):
        """Abstract method returns the name of metric. Used for visualization purposes

        Returns:
            str: Metric name
        """
        ...
