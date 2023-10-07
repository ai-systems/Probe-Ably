#from overrides import overrides
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
from dynaconf import settings
from probe_ably.core.tasks.control_task import GenerateControlTask
from probe_ably.core.models import AbstractModel
from probe_ably.core.metrics import AbstractInterModelMetric, AbstractIntraModelMetric

SCHEMA_TEMPLATE_FILE = settings["input_json_schema"]

class ModelRepresentationFileNotFound(Exception):
    def __init__(self, model_location):
        self.model_location = model_location


class ControlSizeMissmatch(Exception):
    def __init__(self, task_name, model_name):
        self.task_name = task_name
        self.model_name = model_name


class InputClassNotFound(Exception):
    def __init__(self, type_of_class, class_name):
        self.type_of_class = type_of_class
        self.class_name = class_name


class ReadInputTask(Task):
    def run(self, input_file_location: str) -> Dict:
        """Function that parses the input configuration file provided by the user.

        :param input_file_location: Input json file containing the representations for probing and probing setup.
         The file should follow the template in settings["input_json_schema"]
        :type input_file_location: str
        :return: Dictionary of the parsed input, in the following format:
        {
            "tasks": {
               int (task_id):
               {
                   "task_name": str,
                   "models": {
                       int (model_id): {
                           "model_name": str,
                           "model_vectors": array (representations being probed),
                           "model_labels": array (labels for the auxiliary task),
                           "control_labels": array (labels for the control task),
                           "representation_size": int (size of each representation),
                           "number_of_classes": int (number of unique labels),
                           "default_control": boolean (False if user inputs control task)
                       }
                   }
               }
           }

           "probing_setup": {
               "inter_metric": string (class for metric to compare model and control task),
               "intra_metric": string (class for metric that will be used for measuring
                the best model),
               "dev_size": int,
               "train_size": int,
               "test_size": int,
               "probing_models": {
                   int (probing_models_id): {
                       "probing_model_name": string (class for the probing model),
                       "batch_size": int,
                       "epochs": int,
                       "number_of_models": int (number of probe models for generation)
                   }
               }
           }
        }
        :rtype: Dict
        """

        generate_control_task = GenerateControlTask()
        logger.debug("Reading input file.")
        try:
            with open(input_file_location, "r") as f:
                input_data = json.load(f)
                logger.debug(f"Opening file located in {input_file_location}")

            with open(SCHEMA_TEMPLATE_FILE, "r") as f:
                input_template = json.load(f)
            jsonschema.validate(instance=input_data, schema=input_template)

            output_dict = dict()
            current_task_id = 0
            task_list = input_data["tasks"]
            ## Getting input info
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

                    output_dict[current_task_id]["models"][
                        current_model_id
                    ] = self.parse_model_info(
                        model_content, task_content["task_name"], generate_control_task
                    )

                    current_model_id += 1
                current_task_id += 1

            ## Getting probe info
            probing_setup = self.parse_probing_setup(input_data)

        except FileNotFoundError:
            sys.exit(f"Input file not found: {input_file_location}")
        except json.JSONDecodeError as e:
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
        except InputClassNotFound as e:
            sys.exit(
                f"Error in probing setup: Element {e.type_of_class} with content {e.class_name} not found."
            )
        except ValueError as e:
            sys.exit(e)
        return {"tasks": output_dict, "probing_setup": probing_setup}

    @staticmethod
    def parse_model_info(model_content, task_name, generate_control_task):
        model_representation = pd.read_csv(
            model_content["file_location"], sep="\t", header=None
        )
        model_labels = model_representation.iloc[:, -1].to_numpy()

        model_representation.drop(
            model_representation.columns[-1], axis=1, inplace=True
        )
        model_representation = model_representation.to_numpy()

        if "control_location" in model_content:
            default_control = False
            if not os.path.isfile(model_content["control_location"]):
                raise ModelRepresentationFileNotFound(model_content["control_location"])

            control_labels = np.loadtxt(
                fname=model_content["control_location"],
                delimiter="\t",
                dtype=int,
            )

            if len(control_labels) != len(model_labels):
                raise ControlSizeMissmatch(
                    task_name,
                    model_content["model_name"],
                )
        else:
            default_control = True
            logger.info(
                f"No control labels provided for task {task_name} and model {model_content['model_name']}, generating random control task."
            )
            control_labels = generate_control_task.run(
                model_representation, model_labels
            )
        total_number_of_classes = (
            np.amax(np.concatenate((model_labels, control_labels))) + 1
        )
        return {
            "model_name": model_content["model_name"],
            "model_vectors": model_representation,
            "model_labels": model_labels,
            "control_labels": control_labels,
            "representation_size": model_representation.shape[1],
            "number_of_classes": total_number_of_classes,
            "default_control": default_control,
        }

    @staticmethod
    def parse_probing_setup(input_data):
        if "probing_setup" not in input_data:
            with open(settings["default_probing_setup"], "r") as f:
                probing_setup = json.load(f)

            logger.info(
                "No experiment setup provided, using the following default values:"
            )
            logger.info(probing_setup)
        else:
            available_inter_metrics = AbstractInterModelMetric.subclasses
            available_intra_metrics = AbstractIntraModelMetric.subclasses
            available_probing_models = AbstractModel.subclasses

            if (
                input_data["probing_setup"]["inter_metric"]
                not in available_inter_metrics
            ):
                raise InputClassNotFound(
                    "inter_metric", input_data["probing_setup"]["inter_metric"]
                )

            if (
                input_data["probing_setup"]["intra_metric"]
                not in available_intra_metrics
            ):
                raise InputClassNotFound(
                    "intra_metric", input_data["probing_setup"]["intra_metric"]
                )

            split_distribution = (
                input_data["probing_setup"]["train_size"]
                + input_data["probing_setup"]["test_size"]
                + input_data["probing_setup"]["dev_size"]
            )

            if split_distribution != 1:
                raise ValueError(
                    f"Train + Test + Dev size should be equals to 1, got {split_distribution}"
                )
            probing_setup = {
                "inter_metric": input_data["probing_setup"]["inter_metric"],
                "intra_metric": input_data["probing_setup"]["intra_metric"],
                "train_size": input_data["probing_setup"]["train_size"],
                "dev_size": input_data["probing_setup"]["dev_size"],
                "test_size": input_data["probing_setup"]["test_size"],
                "probing_models": dict(),
            }
            num_probing_models = 0

            for probe_model in input_data["probing_setup"]["probing_models"]:
                if probe_model["probing_model_name"] not in available_probing_models:
                    raise InputClassNotFound(
                        "probing_model_name", probe_model["probing_model_name"]
                    )

                probing_setup["probing_models"][num_probing_models] = probe_model
                num_probing_models += 1

            logger.info(
                "Using the experiment setup provided in the input file with values:"
            )
            logger.info(probing_setup)

        return probing_setup