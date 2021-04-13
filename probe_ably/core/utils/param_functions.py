import numpy as np
import random


def nuclear_norm_alpha_generation(num_models, **params):
    return np.array(
        [0]
        + [
            2 ** x
            for x in np.linspace(
                start=params["options"][0],
                stop=params["options"][1],
                num=(num_models - 1),
            )
        ]
    )


def hidden_size_generation(num_models, **params):
    return random.choices(
        list(
            {
                int(2 ** x)
                for x in np.arange(
                    params["options"][0], params["options"][1], params["step"]
                )
            }
        ),
        k=num_models,
    )
