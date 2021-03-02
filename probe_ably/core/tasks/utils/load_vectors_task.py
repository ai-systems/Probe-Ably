from overrides import overrides
from prefect import Task


class LoadVectorsTask(Task):
    @overrides
    def run(self):
        ...
