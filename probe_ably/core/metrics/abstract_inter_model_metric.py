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
    ):
        ...
