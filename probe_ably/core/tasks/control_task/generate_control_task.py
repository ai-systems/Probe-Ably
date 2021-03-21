from overrides import overrides
from prefect import Task
import numpy as np
import pandas as pd


class GenerateControlTask(Task):
    @staticmethod
    def get_unique_labels(labels):
        return np.unique(labels)

    @staticmethod
    def generate_random_labels(unique_labels, labels_size):
        random_labels = np.random.choice(unique_labels, size=labels_size)

        return random_labels

    @overrides
    def run(self, input_data, input_labels, control_type="random"):
        unique_labels = self.get_unique_labels(input_labels)

        output_labels = self.generate_random_labels(unique_labels, len(input_labels))

        return output_labels