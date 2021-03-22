from probe_ably.core.metrics import AbstractInterModelMetric
from sklearn.metrics import accuracy_score


class SelectivityMetric(AbstractInterModelMetric):
    def __init__(self):
        super().__init__()

    def calculate_metrics(
        self, targets1, targets2, predicitons1, predicitons2, **kwargs
    ):
        return accuracy_score(targets1, predicitons1) - accuracy_score(
            targets2, predicitons2
        )

    def metric_name(self):
        return "Selectivity"
