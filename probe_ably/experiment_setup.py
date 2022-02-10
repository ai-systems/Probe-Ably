import asyncio
import pathlib
from typing import Type, TypedDict, List, Union
from probe_ably.probing import TrainProbingTask
from probe_ably.metrics import ProcessMetricTask
from probe_ably.probing.prepare_data import prep_data_from_parsed_json
from probe_ably.utils import ReadInputTask, ProbingConfig, ProbingTask, ProbingInput
from probe_ably.constants import DEFAULT_PROBING_SETUP
from loguru import logger
from dataclasses import dataclass
from torch.utils.data import Dataset
import threading

read_input_task = ReadInputTask()
train_probing_task = TrainProbingTask()
process_metric_task = ProcessMetricTask()

class ProbingExperiment:
    def __init__(self, 
                probing_config: ProbingConfig,
                tasks: Union[ProbingTask, List[ProbingTask]] = [],
                thread: threading.Thread = None):
        self.probing_config = probing_config
        self.tasks = tasks
        self.thread = thread

    def load_tasks(self, tasks: Union[ProbingTask, List[ProbingTask]]):
        self.tasks = tasks

    @classmethod
    def from_parsed_input(cls, parsed_input: ProbingInput, thread=None):
        probing_config = parsed_input["probing_config"]

        if parsed_input["tasks"]:
            logger.info("Loading data from paths in config")

            tasks = prep_data_from_parsed_json(
                        parsed_input["tasks"], 
                        parsed_input["probing_config"]
                        )
        else: 
            tasks = []

        return cls(probing_config, tasks, thread)

    @classmethod
    def from_json(cls, config_path: Union[str, pathlib.Path], thread=None):
        if config_path is "default":
            config_path = DEFAULT_PROBING_SETUP

        with open(config_path) as config_file:
            parsed_input = asyncio.run(read_input_task.run(config_file))

        return cls.from_parsed_input(parsed_input, thread=thread)
        
    def run(self):
        train_results = train_probing_task.run(self.tasks, self.probing_config, self.thread)
        processed_results = process_metric_task.run(
            train_results, self.probing_config
        )

        return processed_results
        # visualization_task.run(processed_results)