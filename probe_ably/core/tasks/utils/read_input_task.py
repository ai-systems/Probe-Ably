from overrides import overrides
from prefect import Task
from typing import Dict
from loguru import logger
import os.path
import json
import sys
import jsonschema
import os.path
import pandas as pd
import numpy as np
from probe_ably.core.tasks.control_task import GenerateControlTask

# TODO add this to a config file
SCHEMA_TEMPLATE = {
    "type": "object",
    "properties": {
        "tasks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "task_name": {"type": "string"},
                    "models": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "model_name": {"type": "string"},
                                "file_location": {"type": "string"},
                                "control_location": {"type": "string"},
                                "control_type": {"type": "string"},
                            },
                            "required": [
                                "model_name",
                                "file_location",
                            ],
                        },
                    },
                },
                "required": ["task_name", "models"],
            },
        }
    },
    "required": ["tasks"],
}


class ModelRepresentationFileNotFound(Exception):
    def __init__(self, model_location):
        self.model_location = model_location


class ControlSizeMissmatch(Exception):
    def __init__(self, task_name, model_name):
        self.task_name = task_name
        self.model_name = model_name


class ReadInputTask(Task):
    @overrides
    def run(self, input_file_location: str) -> Dict:
        """Function that parses the input configuration file provided by the user.

        Args:
            input_file_location (str): location of the input file

        Returns: Dict:
            Dict:
            { task_id:  {'task_name': str,
                            'models':
                                    {model_id:
                                            {"model_name": str,
                                            "model_vectors": numpy.ndarray
                                            "model_labels": numpy.ndarray
                                            "control_labels": numpy.ndarray
                                             }
                                    }
                    }
        """

        generate_control_task = GenerateControlTask()
        logger.debug("Reading input file.")
        try:
            with open(input_file_location, "r") as f:
                input_data = json.load(f)
                logger.debug(f"Opening file located in {input_file_location}")

            jsonschema.validate(instance=input_data, schema=SCHEMA_TEMPLATE)

            output_dict = dict()
            current_task_id = 0
            task_list = input_data["tasks"]
            for task_content in task_list:
                output_dict[current_task_id] = dict()
                output_dict[current_task_id]["task_name"] = task_content["task_name"]
                output_dict[current_task_id]["models"] = dict()
                models_list = task_content["models"]

                current_model_id = 0
                for model_content in models_list:
                    if not os.path.isfile(model_content["file_location"]):
                        raise ModelRepresentationFileNotFound(
                            model_content["file_location"]
                        )
                    else:
                        model_representation = pd.read_csv(
                            model_content["file_location"], sep="\t", header=None
                        )
                        model_labels = model_representation.iloc[:, -1].to_numpy()

                        model_representation.drop(
                            model_representation.columns[-1], axis=1, inplace=True
                        )
                        model_representation = model_representation.to_numpy()

                    if "control_location" in model_content:
                        if not os.path.isfile(model_content["control_location"]):
                            raise ModelRepresentationFileNotFound(
                                model_content["control_location"]
                            )
                        else:
                            control_labels = np.loadtxt(
                                fname=model_content["control_location"],
                                delimiter="\t",
                                dtype=int,
                            )

                            if len(control_labels) != len(model_labels):
                                raise ControlSizeMissmatch(
                                    output_dict[current_task_id]["task_name"],
                                    model_content["model_name"],
                                )
                    else:
                        if "control_type" in model_content:
                            control_labels = generate_control_task.run(
                                model_representation,
                                model_labels,
                                model_content["control_type"],
                            )
                        else:
                            control_labels = generate_control_task.run(
                                model_representation, model_labels
                            )

                    output_dict[current_task_id]["models"][current_model_id] = {
                        "model_name": model_content["model_name"],
                        "model_vectors": model_representation,
                        "model_labels": model_labels,
                        "control_labels": control_labels,
                    }

                    current_model_id += 1
                current_task_id += 1

        except FileNotFoundError:
            sys.exit(f"Input file not found: {input_file_location}")
        except json.JSONDecodeError:
            sys.exit(
                f"Input file is not a properly foramtted json file: {input_file_location}"
            )
        except jsonschema.ValidationError as e:
            logger.error(e)
            sys.exit(
                f"Input file ({input_file_location}) does not follow correct template. Please refer to README file."
            )
        except ModelRepresentationFileNotFound as e:
            sys.exit(f"Representation file ({e.model_location}) not found.")

        except ControlSizeMissmatch as e:
            sys.exit(
                f"Control task for task {e.task_name} and model {e.model_name} does not match the number of labels of the aux task."
            )

        return output_dict
