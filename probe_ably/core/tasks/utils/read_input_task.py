from overrides import overrides
from prefect import Task
from typing import Dict
from loguru import logger
import os.path
import json
import sys
import jsonschema
import os.path


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


class ReadInputTask(Task):
    @overrides
    def run(self, input_file_location: str) -> Dict:
        """Function that parses the input configuration file provided by the user.

        Args:
            input_file_location (str): location of the input file

        Returns: Dict:
            Dict:
                {'tasks':
                    { task_id: int : {'task_name': str,
                                        'models':
                                                {model_id:
                                                        {'model_name': str,
                                                         'file_location': str,
                                                         'control_type: 0 [Random], 1 [Special], 2 [User Gen]
                                                         'control_location': str [If user generated] or None
                                                }
                                    }
                    }
                }
        """

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

                    control_type = 0
                    control_location = None
                    if "control_location" in model_content:
                        if not os.path.isfile(model_content["control_location"]):
                            raise ModelRepresentationFileNotFound(
                                model_content["file_location"]
                            )
                        control_location = model_content["control_location"]
                        control_type = 2

                    if "control_type" in model_content and control_location == None:
                        if model_content["control_type"] == "special":
                            control_type = 1

                    output_dict[current_task_id]["models"][current_model_id] = {
                        "model_name": model_content["model_name"],
                        "file_location": model_content["file_location"],
                        "control_type": control_type,
                        "control_location": control_location,
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
