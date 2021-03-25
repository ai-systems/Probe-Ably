from abc import ABC, abstractmethod


class AbstractInterModelMetric(ABC):

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
    def calculate_metrics(
        self, targets1, targets2, predicitons1, predicitons2, **kwargs
    ) -> float:
        """Abstract method that calcuate the inter model metric

        Args:
            targets1 (np.array): Gold labels of first set of data
            targets2 (np.array): Gold labels of second set of data
            predicitons1 (np.array): Predictions of first set of data
            predicitons2 (np.array): Predictions of second set of data

        Returns:
            float: Inter model metric score
        """
        ...

    @abstractmethod
    def metric_name(self):
        """Abstract method returns the name of metric. Used for visualization purposes

        Returns:
            str: Metric name
        """
        ...
