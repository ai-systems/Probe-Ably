import asyncio
from numpy import arange

import torch
from torch.utils.data import Dataset
from dataclasses import dataclass
from typing import List, Dict, TypedDict
from numpy.typing import ArrayLike
from probe_ably.probing import PrepareDataForProbingTask, TrainProbingTask
from probe_ably.metrics import ProcessMetricTask
from probe_ably.utils import ReadInputTask

read_input_task = ReadInputTask()
prepare_data_probing = PrepareDataForProbingTask()
train_probing_task = TrainProbingTask()
process_metric_task = ProcessMetricTask()

class RepresentationDataset(TypedDict):
    representations: torch.Tensor
    labels: ArrayLike

class RepresentationSplits(TypedDict):
    train: RepresentationDataset
    dev: RepresentationDataset
    test: RepresentationDataset

class RepresentationSplitDataset(TypedDict):
    representation_name: str
    split_representation: RepresentationSplits
    control: RepresentationSplits
    representation_size: int
    number_of_classes: int
    default_control: bool
    
class ProbingTask(TypedDict):
    task_name: str
    representations: List(RepresentationSplitDataset)

class ProbingExperimentData(TypedDict): 
    tasks: List(ProbingTask)

@dataclass
class ProbingExperiment():
    def __init__(self) -> None:
        self.prepared_data = None
        self.probing_setup = None

    def from_files(self, config_file: str):
        """
        Setup data and probing configuration from a single config file, 
        referencing filepaths of representation files.

        Parameters
        ----------
        config_file : str
            [description]
        """

        parsed_input = asyncio.run(read_input_task.run(config_file))
        self.prepared_data = prepare_data_probing.run(
            parsed_input["tasks"], parsed_input["probing_setup"]
        )
        self.probing_setup = parsed_input["probing_setup"]

    def from_splits(train_reps, dev_reps, test_reps,
                        train_labels, dev_labels, test_labels,
                        control_train_labels=None,
                        control_dev_labels=None,
                        control_test_labels=None,
                    )-> RepresentationSplitDataset:


    def from_reps_labels(representation: torch.tensor,
                            labels: ArrayLike
                        )->RepresentationDataset: