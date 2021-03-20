from overrides import overrides
from prefect import Task


class RunProbingTask(Task):
    def run(self, input_data):
        """Run probing task for the required models

        Args:


            {"tasks": { task_id: int : {'task_name': str,
                                        'models':
                                                {model_id:
                                                        {'model_name': str,
                                                         'representation':
                                                         'representation_labels':
                                                         'control_labels':
                                                }
                                    }
            }

        Return:
            {"tasks": { task_id: int : {'task_name': str,
                                        probing_models :{ id:{ "probing_name": xxxxx
                                                                "models": id: { "name": xxxx
                                                                                "acc_aux": xxxx
                                                                                "acc_control:" xxxx
                                                                                "complexity": xxxx
                                                                                "selectivity": xxxx
                                                                }
                                        }

        """
