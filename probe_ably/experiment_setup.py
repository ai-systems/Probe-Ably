import asyncio
from uvicorn import config
from typing import TypedDict
from collections import NamedTuple
from probe_ably.probing import PrepareDataForProbingTask, TrainProbingTask
from probe_ably.metrics import ProcessMetricTask
from probe_ably.utils import ReadInputTask
from probe_ably.constants import DEFAULT_PROBING_SETUP
from loguru import logger
from dataclasses import dataclass
f

read_input_task = ReadInputTask()
prepare_data_probing = PrepareDataForProbingTask()
train_probing_task = TrainProbingTask()
process_metric_task = ProcessMetricTask()


class ProbingConfig():
    # list of probing models
    self.train_size=None
    self.dev_size=None
    self.config_tasks = None
    #validate

    @classmethod
    def from_json_file(cls, config_path):
        if config_path is "default":
            config_path = asyncio.run(read_input_task.run(DEFAULT_PROBING_SETUP))

        with open(config_path) as config_file:
            parsed_input = asyncio.run(read_input_task.run(config_file))
            probing_setup = parsed_input["probing_setup"]

            if parsed_input["tasks"]:
                config_tasks = parsed_input["tasks"]

class ProbingData():
    @classmethod
    def from_config(config: ProbingConfig):
        probing_data = prepare_data_probing.run(
            config.tasks, config.probing_setup)



class ProbingExperiment():
    def __init__(self, config_path, tasks: List[ProbingTask]) -> None:
        # Optionally:
        self.probing_data = None

    @classmethod
    def from_config(cls, config_path):
        if config_path is "default":
            config_path = asyncio.run(read_input_task.run(DEFAULT_PROBING_SETUP))

        with open(config_path) as config_file:
            parsed_input = asyncio.run(read_input_task.run(config_file))
            config = parsed_input["probing_setup"]

            if parsed_input["tasks"]:
                probing_data = prepare_data_probing.run(
                    parsed_input["tasks"], parsed_input["probing_setup"]



class ProbingExperiment():
    def __init__(self, probing_data: ProbingData, probing_config: ProbingConfig) -> None:
        self.probing_data = probing_data
        self.probing_config = probing_config

    @classmethod
    def from_config(cls, config_path: str = "default"):
        """
        [summary]

        Parameters
        ----------
        config_path : str
            [description]

        """        
        # if parsed_input["tasks"]:
        #     logger.info("Loaded data from paths in config")
        #     self.prepared_data = prepare_data_probing.run(
        #         parsed_input["tasks"], parsed_input["probing_setup"]
        #     )

    def run(self, probing_data: ProbingData):
        train_results = train_probing_task.run(self.prepared_data, self.probing_setup)
        processed_results = process_metric_task.run(
            train_results, self.probing_setup
        )
        # visualization_task.run(processed_results)

@task
def prep_data_for_probeably(all_data_encodings, encode_configs)->:
    """
    :return: Dictonary of processed data in the format:
    { task_id:
        {'task_name': str,
        'models':
            {model_id:
                {"model_name": str,
                    "model": {"train":,  
                              "dev": , 
                              "test": },
                    "control": {"train": , 
                                "dev": , 
                                "test": },
                    "representation_size": int,
                    "number_of_classes": int,
                    "default_control": boolean (False if user inputs control task)
                }
            }
        }
        ...
    }
    :rtype: Dict
    """

    task_labels = encode_configs['shared_config']['task_labels']
    all_prepared_task_data = [prep_task_data_for_probeably.run(all_data_encodings, 
                                        task_label, encode_configs) for task_label in task_labels]

    return dict(enumerate(all_prepared_task_data))

@task
def prep_task_data_for_probeably(all_data_encodings, task_label, encode_configs):

    prepared_task_data = {
            "task_name": task_label,
            "models": dict(enumerate([prepare_model_contents(rep_name, 
                                        task_label,
                                        encode_configs, 
                                        all_data_encodings) 
                                        for rep_name in all_data_encodings.keys()]))
        }

    return prepared_task_data


def prepare_model_contents(rep_name, task_label, encode_configs, all_data_encodings):
    encoded_data = all_data_encodings[rep_name]

    splits = ['train', 'dev', 'test']

    model_data_dict = dict(zip(splits, 
                          [prepare_entries(encoded_data, 
                                           split, 
                                           task_label, 
                                           encode_configs) for split in splits]))
    control_data_dict = dict(zip(splits, 
                          [prepare_entries(encoded_data, 
                                           split, 
                                           task_label, 
                                           encode_configs,
                                           control=True) for split in splits]))
    return {"model_name": rep_name,
                "model": model_data_dict,
                "control": control_data_dict,
                "representation_size": encoded_data["train"]["representations"].shape[1],
                "number_of_classes": get_num_classes(task_label, encoded_data),
                "default_control": False
	}

def prepare_entries(encoded_data, split, task_label, encode_configs, control=False):
    encoded_data_split = encoded_data[split]
    vectors = encoded_data_split["representations"].to('cpu')

    if not control:
        try:
            categorical_labels = encoded_data_split["meta_df"][task_label]
            try:
                labels = torch.tensor(categorical_labels.values,
                                    dtype=torch.long).to('cpu')
            except:
                coded_labels = categorical_labels.apply(lambda x: relabel(x, task_label))
                labels = torch.tensor(coded_labels.values,
                                        dtype=torch.long).to('cpu')
        except KeyError:
            raise ValueError(f'''Invalid task label {task_label}
            specified, not found in meta dataframe columns!''')
    elif control:
        labels = load_control_labels_from_file(task_label, encode_configs, split)
    else:
        raise ValueError(f'No valid labels for {task_label}!')

    dataset = dict()
    for i in range(0, len(vectors)):
        dataset[i] = {"representation": vectors[i], "label": labels[i]}

    return TorchDataset(dataset)


class ProbingData(TypedDict):
    tasks: List[ProbingTask]
    probing_setup: ProbingConfig

class ProbingTask(TypedDict):
    task_name: str
    representations: List[ProbingRepresentation]