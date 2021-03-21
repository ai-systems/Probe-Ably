from typing import Any, Dict, List

from probe_ably.core.models import AbstractModel
import importlib
import random
import os
import glob
import json

class GridModelFactory:
    @staticmethod
    def create_models(model_class: str, num_models: int = 50, param_args:Dict = {})-> List[AbstractModel]:

        paths = glob.glob("./config/params/*.json")
        print(paths)

        params = None 
        for path in paths:
            with open(path, 'r') as f:
                maybe_params = json.load(f)
                print(model_class)
                print(maybe_params)
                if model_class in maybe_params:
                    params = maybe_params[model_class]['params']
                    break
        if not params:
            raise FileNotFoundError('No parameters specified, dear.')

        ModelClass = AbstractModel.subclasses[model_class]

        models = []
        for i in range(num_models):
            chosen_params = choose_params(params)
            model = ModelClass({**chosen_params, **param_args})
            models.append(model)

        return models


def choose_params(params: List[Dict]):
    names = [param['name'] for param in params]
    values = [random.uniform(*param['bounds']) for param in params]
    return dict(zip(names, values))
    

if __name__=='__main__':
    params = [{'name':'dog', 'bounds':[0.1, 20.3]},{'name':'cat', 'bounds':[0.2, 0.5]}]

    choose_params(params)
