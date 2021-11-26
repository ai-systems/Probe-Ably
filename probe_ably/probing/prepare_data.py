from overrides import overrides
from prefect import Task
from loguru import logger
import sklearn
from sklearn.model_selection import train_test_split
from typing import Dict
import torch
from torch.utils.data import Dataset
import numpy as np
from probe_ably.utils.input_types import SplitProbingDataset, ProbingRepresentation, ProbingInput, ProbingConfig, ProbingTask

def prepare_probing_dataset(vectors, labels) -> Dataset:
    dataset = dict()
    for i in range(0, len(vectors)):
        dataset[i] = {"representation": vectors[i], "label": labels[i]}
    return TorchDataset(dataset)

def train_val_test_split(X, y, train_size, val_size, test_size, seed=42):
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed
    )
    relative_train_size = train_size / (val_size + train_size)

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val,
        y_train_val,
        test_size=1 - relative_train_size,
        random_state=seed,
    )

    return X_train, X_val, X_test, y_train, y_val, y_test

def unpack_rep_data(rep_content: dict, probing_config: ProbingConfig) -> ProbingRepresentation:
    print(rep_content)
    (
        model_vectors_train,
        model_vectors_val,
        model_vectors_test,
        model_labels_train,
        model_labels_val,
        model_labels_test,
    ) = train_val_test_split( X=rep_content["representation_vectors"], y=rep_content["representation_labels"],
        train_size=probing_config["train_size"],
        val_size=probing_config["dev_size"],
        test_size=probing_config["test_size"],
    )
    (
        control_vectors_train,
        control_vectors_val,
        control_vectors_test,
        control_labels_train,
        control_labels_val,
        control_labels_test,
    ) = train_val_test_split(
        X=rep_content["representation_vectors"],
        y=rep_content["control_labels"],
        train_size=probing_config["train_size"],
        val_size=probing_config["dev_size"],
        test_size=probing_config["test_size"],
    )

    representation_dataset: SplitProbingDataset = {
        "train": prepare_probing_dataset(
            model_vectors_train, model_labels_train
        ),
        "dev": prepare_probing_dataset(model_vectors_val, model_labels_val),
        "test": prepare_probing_dataset(model_vectors_test, model_labels_test),
    }
    control_dataset: SplitProbingDataset = {
        "train": prepare_probing_dataset(
            control_vectors_train, control_labels_train
        ),
        "dev": prepare_probing_dataset(
            control_vectors_val, control_labels_val
        ),
        "test": prepare_probing_dataset(
            control_vectors_test, control_labels_test
        ),
    }

    representation: ProbingRepresentation = {
        "representation_name": rep_content["representation_name"],
        "representation_size": rep_content["representation_size"],
        "number_of_classes": rep_content["number_of_classes"],
        "default_control": rep_content["default_control"],
        "representation": representation_dataset,
        "control":control_dataset,
    }
    return representation

def prep_data_from_parsed_json(parsed_tasks_data: Dict, probing_config: ProbingConfig, return_trained_model: bool = False) -> Dict:
    """Reads the task_data and experiment_setup, splits into train/dev/test and
    creates a TorchDataset for each.

    :param tasks_data: Tasks info obtained from user input
    :type tasks_data: Dict
    :param experiment_setup: Experiment setup obtained from default file or user input
    :type experiment_setup: Dict
    :return: Dictonary of processed data in the format:
    { task_id:
        {'task_name': str,
        'models':
            {model_id:
                {"model_name": str,
                    "model": {"train": numpy.ndarray, "dev": numpy.ndarray, "test": numpy.ndarray},
                    "control": {"train": numpy.ndarray, "dev": numpy.ndarray, "test": numpy.ndarray},
                    "representation_size": int,
                    "number_of_classes": int,
                    "default_control": boolean (False if user inputs control task)
                }
            }
        }
    }
    :rtype: Dict
    """

    logger.debug("Prepare the data for probing.")

    tasks = list() 
    for id_task, task_content in parsed_tasks_data.items():
        probing_task : ProbingTask = {
            "task_name": task_content["task_name"],
            "representations": [unpack_rep_data(rep_content, probing_config) for rep_id, rep_content in task_content["representations"].items()]
            }
        tasks.append(probing_task)

    return tasks

class TorchDataset(Dataset):
    def __init__(self, dataset):
        self.dataset = list(dataset.values())
        self.labels = np.array([data["label"] for data in self.dataset])
        self.keys = list(dataset.keys())

    def __getitem__(self, index):
        instance = self.dataset[index]
        return (
            torch.FloatTensor(instance["representation"]),
            instance["label"],
            index,
        )

    def get_id(self, index):
        return self.keys[index]

    def __len__(self):
        return len(self.dataset)