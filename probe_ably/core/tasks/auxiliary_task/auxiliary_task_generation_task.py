from overrides import overrides
from prefect import Task


class AuxiliaryTaskGenerationTask(Task):
    def run(self, input_data):
        """Loads the contents of the file as auxiliary tasks and control tasks

        Args:
            input_data (Dict):  Returns: Dict:
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

        Return

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

        """
