import numpy as np
from probe_ably.metrics import AbstractIntraModelMetric
from sklearn.metrics import accuracy_score


class AccuracyMetric(AbstractIntraModelMetric):
    def calculate_metrics(
        self, targets: np.array, predicitons: np.array, **kwargs
    ) -> float:
        """Calculates and returns accruacy score

        Args:
            targets (np.array): Gold target scores
            predicitons (np.array): Predictions data

        Returns:
            float: Returns accuracy score
        """
        return accuracy_score(targets, predicitons)

    def metric_name(self):
        """Returns the name of metric. Used for visualization purposes

        Returns:
            str: Metric name
        """
        return "Accuracy"
