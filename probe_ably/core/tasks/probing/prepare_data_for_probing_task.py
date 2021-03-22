from overrides import overrides
from prefect import Task
from loguru import logger
import sklearn
from sklearn.model_selection import train_test_split
from typing import Dict
import torch
from torch.utils.data import Dataset
import numpy as np


class PrepareDataFromProbingTask(Task):
    # TODO Add some comments
    @staticmethod
    def prepare_entries(vectors, labels):
        dataset = dict()
        for i in range(0, len(vectors)):
            dataset[i] = {"representation": vectors[i], "label": labels[i]}

        return TorchDataset(dataset)

    # TODO Add split sizes to a config file
    @staticmethod
    def train_val_test_split(
        X, y, train_size=0.5, val_size=0.2, test_size=0.3, seed=42
    ):
        X_train_val, X_test, y_train_val, y_test = train_test_split(
            X, y, test_size=test_size, random_state=seed
        )
        relative_train_size = train_size / (val_size + train_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_val,
            y_train_val,
            train_size=relative_train_size,
            test_size=1 - relative_train_size,
            random_state=seed,
        )
        return X_train, X_val, X_test, y_train, y_val, y_test

    # TODO ADd proper comments here
    @overrides
    def run(self, tasks_data: Dict) -> Dict:
        """[summary]

        Args:
            tasks_data (Dict):
            { task_id:  {'task_name': str,
                    'models':
                            {model_id:
                                    {"model_name": str,
                                    "model_vectors": numpy.ndarray
                                    "model_labels": numpy.ndarray
                                    "control_labels": numpy.ndarray
                                    "representation_size": int
                                    "number_of_classes": int
                                     }
                            }
            }

        Returns:
            Dict: output_data
            {task_id: {"task_name": str,
                        "models": {model_id: {
                                    "model_name": str,
                                    "model": { "train": TorchDataset, "dev": TorchDataset, "test": TorchDataset }
                                    "control": { "train": TorchDataset, "dev": TorchDataset, "test": TorchDataset }
                                    }
                                }
                        }
                }
        """

        logger.debug("Prepare the data for probing.")
        output_data = dict()

        for id_task, task_content in tasks_data.items():
            output_data[id_task] = dict()
            output_data[id_task]["task_name"] = task_content["task_name"]
            output_data[id_task]["models"] = dict()
            for model_id, model_content in task_content["models"].items():
                output_data[id_task]["models"][model_id] = dict()
                output_data[id_task]["models"][model_id][
                    "representation_size"
                ] = model_content["representation_size"]

                output_data[id_task]["models"][model_id][
                    "number_of_classes"
                ] = model_content["number_of_classes"]

                output_data[id_task]["models"][model_id]["model_name"] = model_content[
                    "model_name"
                ]

                (
                    model_vectors_train,
                    model_vectors_val,
                    model_vectors_test,
                    model_labels_train,
                    model_labels_val,
                    model_labels_test,
                ) = self.train_val_test_split(
                    model_content["model_vectors"], model_content["model_labels"]
                )

                output_data[id_task]["models"][model_id]["model"] = {
                    "train": self.prepare_entries(
                        model_vectors_train, model_labels_train
                    ),
                    "dev": self.prepare_entries(model_vectors_val, model_labels_val),
                    "test": self.prepare_entries(model_vectors_test, model_labels_test),
                }

                (
                    control_vectors_train,
                    control_vectors_val,
                    control_vectors_test,
                    control_labels_train,
                    control_labels_val,
                    control_labels_test,
                ) = self.train_val_test_split(
                    model_content["model_vectors"], model_content["control_labels"]
                )

                output_data[id_task]["models"][model_id]["control"] = {
                    "train": self.prepare_entries(
                        control_vectors_train, control_labels_train
                    ),
                    "dev": self.prepare_entries(
                        control_vectors_val, control_labels_val
                    ),
                    "test": self.prepare_entries(
                        control_vectors_test, control_labels_test
                    ),
                }

        return output_data


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
