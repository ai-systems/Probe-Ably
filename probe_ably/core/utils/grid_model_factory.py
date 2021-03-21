from typing import Any, Dict, List

from probe_ably.core.models import AbstractModel


class GridModelFactory:
    @staticmethod
    def create_models(model: str, params:List[Dict], num_models: int = 50)-> List[AbstractModel]:
        ...



