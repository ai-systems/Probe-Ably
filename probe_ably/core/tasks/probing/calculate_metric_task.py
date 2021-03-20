from overrides import overrides
from prefect import Task


class CalculateMetricTask(Task):
    @overrides
    def run(self):
        ...
