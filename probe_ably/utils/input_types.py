from typing import Type, TypedDict, List, Union, Dict
from torch.utils.data import Dataset

class ProbingConfig(TypedDict):
    train_size: float
    dev_size: float
    test_size: float
    inter_metric: Union[str, List[str]]
    intra_metric: Union[str, List[str]]
    probing_models: List[Dict]
    
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
    '''

    '''
    task_name: str
    representations: List[ProbingRepresentation]

class ProbingInput(TypedDict):
    tasks: List[ProbingTask]
    probing_setup: ProbingConfig