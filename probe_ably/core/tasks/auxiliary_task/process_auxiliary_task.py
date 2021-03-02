from overrides import overrides
from prefect import Task


class ProcessAuxiliaryTask(Task):
    @overrides
    def run(self):
        ...
