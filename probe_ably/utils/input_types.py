from typing import Type, TypedDict, List, Union, Dict
from torch.utils.data import Dataset

class ProbingConfig(TypedDict):
    probing_models: List[Dict]
    inter_metric: Union[str, List[str]]
    intra_metric: Union[str, List[str]]
    own_splits: bool
    train_size: float
    dev_size: float
    test_size: float

class SplitProbingDataset(TypedDict):
    train: Dataset
    dev: Dataset
    test: Dataset

class ProbingRepresentation(TypedDict):
    representation_name: str
    representation: SplitProbingDataset
    control: SplitProbingDataset
    representation_size: int
    number_of_classes: int
    default_control: bool 


class ProbingTask(TypedDict):
    task_name: str
    representations: List[ProbingRepresentation]

class ProbingInput(TypedDict):
    tasks: List[ProbingTask]
    probing_config: ProbingConfig