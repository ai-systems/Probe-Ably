from overrides import overrides
from prefect import Task


class TrainProbingTask(Task):
    @overrides
    def run(self):
        ...
