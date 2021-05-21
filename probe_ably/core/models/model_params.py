from typing import Dict

class ModelParams():
    def __init__(self)->Dict:
        self.default_params = {
            "probe_ably.core.models.linear.LinearModel": { 
                "params": [
                        {
                        "name": "dropout",
                        "type": "float_range",
                        "options": [0.0, 0.51]
                    },
                        {
                        "name": "alpha",
                        "type": "function",
                        "function_location": "probe_ably.core.utils.param_functions.nuclear_norm_alpha_generation",
                        "options": [-10.0, 3]
                    }]
            }, 
            "probe_ably.core.models.mlp.MLPModel": {
                "params": [
                    {
                        "name": "hidden_size",
                        "type": "function",
                        "step": 0.01,
                        "function_location": "probe_ably.core.utils.param_functions.hidden_size_generation",
                        "options": [
                            2,
                            5
                        ]
                    },
                    {
                        "name": "n_layers",
                        "type": "int_range",
                        "options": [
                            1,
                            2 
                        ]
                    },
                    {
                        "name": "dropout",
                        "type": "float_range",
                        "options": [
                            0.0,
                            0.5
                        ]
                    }
                ]
            }
        }