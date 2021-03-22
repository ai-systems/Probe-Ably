from probe_ably.core.metrics import AbstractIntraModelMetric
from sklearn.metrics import accuracy_score


class AccuracyMetric(AbstractIntraModelMetric):
    def __init__(self):
        super().__init__()

    def calculate_metrics(self, targets, predicitons, **kwargs):
        return accuracy_score(targets, predicitons)
