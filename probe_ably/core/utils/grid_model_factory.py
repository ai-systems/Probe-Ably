from typing import Any, Dict, List

from probe_ably.core.models import AbstractModel
import importlib
import random

class GridModelFactory:

    @staticmethod
    def create_models(model_class: str, params: List[Dict], num_models: int = 50)-> List[AbstractModel]:

        ModelClass = AbstractModel.subclasses[model_class]

        models = []
        for i in range(num_models):
            chosen_params = choose_params(params)
            model = ModelClass(chosen_params)
            models.append(model)

        return models


def choose_params(params: List[Dict]):
    names = [param['name'] for param in params]
    values = [random.uniform(*param['bounds']) for param in params]
    return dict(zip(names, values))
    

if __name__=='__main__':
    params = [{'name':'dog', 'bounds':[0.1, 20.3]},{'name':'cat', 'bounds':[0.2, 0.5]}]

    choose_params(params)