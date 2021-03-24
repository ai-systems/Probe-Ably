from typing import Any, Dict, List

from probe_ably.core.models import AbstractModel
import importlib
import numpy as np
import random
import os
import glob
import json


class GridModelFactory:
    @staticmethod
    def create_models(
        model_class: str, num_models: int = 50, param_args: Dict = {}
    ) -> List[AbstractModel]:

        paths = glob.glob("./config/params/*.json")

        params = None
        for path in paths:
            with open(path, "r") as f:
                maybe_params = json.load(f)
                if model_class in maybe_params:
                    params = maybe_params[model_class]["params"]
                    break
        if not params:
            raise FileNotFoundError("No parameters specified, dear.")

        ModelClass = AbstractModel.subclasses[model_class]

        models = []
        for i in range(num_models):
            chosen_params = choose_params(params)
            model = ModelClass({**chosen_params, **param_args})
            models.append(model)

        return models


def choose_params(params: List[Dict]):
    names = [param["name"] for param in params]
    values = [choose_one_param_value(param) for param in params]
    return dict(zip(names, values))


def choose_one_param_value(param):
    if param["type"] == "float_range":
        value = random.uniform(float(param["options"][0]), float(param["options"][1]))
    elif param["type"] == "int_range":
        value = random.randint(int(param["options"][0]), int(param["options"][1]))
    elif param["type"] == "categorical":
        value = np.random_choice(param["options"])
    else:
        raise ValueError(f"Invalid or no value options for parameter {params['name']}")

    try:
        if param['transform']=='2**x':
            value= 2**(value)
    except KeyError:
        pass

    return value
