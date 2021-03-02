from overrides import overrides
from prefect import Task


class GenerateRandomTask(Task):
    def run(self):
        ...
