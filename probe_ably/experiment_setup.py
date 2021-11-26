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
    def __init__(self, tasks: Union[ProbingTask, List[ProbingTask]],
                    probing_config: ProbingConfig,
                    thread: threading.Thread = None) -> None:
        self.probing_config = probing_config
        self.tasks = tasks
        self.thread = thread

    @classmethod
    def from_json(cls, config_path: Union[str, pathlib.Path]):
        if config_path is "default":
            config_path = DEFAULT_PROBING_SETUP

        with open(config_path) as config_file:
            parsed_input = asyncio.run(read_input_task.run(config_file))
            probing_config = parsed_input["probing_config"]

            if parsed_input["tasks"]:
                logger.info("Loading data from paths in config")

                tasks = prep_data_from_parsed_json(
                            parsed_input["tasks"], 
                            parsed_input["probing_config"]
                            )
            else: 
                tasks = []

        return cls(tasks, probing_config, thread)
        
    def run(self):
        train_results = train_probing_task.run(self.tasks, self.probing_config)
        processed_results = process_metric_task.run(
            train_results, self.probing_config
        )
        # visualization_task.run(processed_results)