import numpy as np
from probe_ably.metrics import AbstractInterModelMetric
from sklearn.metrics import accuracy_score


class SelectivityMetric(AbstractInterModelMetric):
    def calculate_metrics(
        self,
        targets1: np.array,
        targets2: np.array,
        predicitons1: np.array,
        predicitons2: np.array,
        **kwargs
    ) -> float:
        """Calculates the selectivity metric

        Args:
            targets1 (np.array): Gold labels of first set of data
            targets2 (np.array): Gold labels of second set of data
            predicitons1 (np.array): Predictions of first set of data
            predicitons2 (np.array): Predictions of second set of data

        Returns:
            float: Selectivity score
        """
        return accuracy_score(targets1, predicitons1) - accuracy_score(
            targets2, predicitons2
        )

    def metric_name(self) -> str:
        """Returns the name of metric. Used for visualization purposes

        Returns:
            str: Metric name
        """
        return "Selectivity"
