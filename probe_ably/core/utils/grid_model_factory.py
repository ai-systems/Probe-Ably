from typing import Any, Dict, List

from probe_ably.core.models import AbstractModel


class GridModelFactory:

    @staticmethod
    def create_models(representation_size:int, n_classes:int, model:str, params:List[Dict], num_models: int = 50)-> List[AbstractModel]:
        ...



