import importlib
import random
from typing import Any, Dict, List
import numpy as np
from probe_ably.models import AbstractModel, ModelParams


class GridModelFactory:
    @staticmethod
    def create_models(
        model_class: str, num_models: int = 50, param_args: Dict = {}
    ) -> List[AbstractModel]:
        """Creates a list of models provided from static param ranges

        Args:
            model_class (str): Probing model class. For example: :code:`probe_ably.models.linear`
            num_models (int, optional): Number of Models to create. Defaults to 50.
            param_args (Dict, optional): Paramter ranges to choose from the model to create. Defaults to {}.

        Returns:
            List[AbstractModel]: Creates a Grid with the prescribed parameter ranges and returns list of models with size num_models by random initialization
        """

        ModelClass = AbstractModel.subclasses[model_class]
        params = ModelParams().default_params[model_class]["params"]

        generated_params = dict()
        for param in params:
            if param["type"] == "function":
                p, m = param["function_location"].rsplit(".", 1)
                module_path = importlib.import_module(p)
                generator_function = getattr(module_path, m)
                generated_params[param["name"]] = generator_function(
                    num_models=num_models, **param
                )
            elif param["type"] == "float_range":
                generated_params[param["name"]] = np.random.uniform(
                    low=float(param["options"][0]),
                    high=float(param["options"][1]),
                    size=(num_models,),
                )
            elif param["type"] == "int_range":
                generated_params[param["name"]] = random.choices(
                    range(int(param["options"][0]), int(param["options"][1])),
                    k=num_models,
                )

            elif param["type"] == "categorical":
                generated_params[param["name"]] = random.choices(
                    param["options"], k=num_models
                )

        chosen_params_dict = dict()
        for i in range(num_models):
            chosen_params_dict[i] = dict()
            for key_name, values in generated_params.items():
                chosen_params_dict[i][key_name] = values[i]

        models = []
        for i in range(num_models):
            model = ModelClass({**chosen_params_dict[i], **param_args})
            models.append(model)

        return models


# def _choose_params(params: List[Dict]):
#     ""
#     names = [param["name"] for param in params]
#     values = [_choose_one_param_value(param) for param in params]
#     return dict(zip(names, values))


# def _choose_one_param_value(param):
#     ""
#     if param["type"] == "float_range":
#         value = random.uniform(float(param["options"][0]), float(param["options"][1]))
#     elif param["type"] == "int_range":
#         value = random.randint(int(param["options"][0]), int(param["options"][1]))
#     elif param["type"] == "categorical":
#         value = np.random_choice(param["options"])
#     else:
#         raise ValueError(f"Invalid or no value options for parameter {params['name']}")

#     try:
#         if param["transform"] == "2**x":
#             value = 2 ** (value)
#     except KeyError:
#         pass

#     return value
