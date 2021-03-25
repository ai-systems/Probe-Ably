Probing Models
##############


Available Models
*****************

Linear Model
============

**Model Name**:  probe_ably.core.models.linear.LinearModel

.. automodule:: probe_ably.core.models.linear
    :members:
    :special-members: __init__

Here :code:`representation_size` and :code:`n_classes` will be provided during runtime by the trainer initated from the data.
:code:`dropout` and :code:`alpha` values are static value ranges are provided in **config/params/linear.json** file.
The :code:`probe_ably.core.utils.grid_model_factory` (See `Grid Model Factory <../utils/grid_factory.html>`_) creates multiple models with the prescribe values for probing.

**config/params/linear.json** is defined as follows:

.. code-block:: json

    {
        "probe_ably.core.models.linear.LinearModel":{
            "params":[
                {
                    "name":"dropout",
                    "type":"float_range",
                    "options":[
                    0.0,
                    0.51
                    ]
                },
                {
                    "name":"alpha",
                    "transform":"2**x",
                    "type":"float_range",
                    "options":[
                    -10.0,
                    3.0
                    ]
                }
            ]
        }
    }

    

Here the ranges of :code:`__init__` static params is as follows:

- :code:`dropout` is of float range between 0.0 and 0.51
- :code:`alpha` is of float range between 2 :superscript:`-10.0` and 2 :superscript:`3.0`



Multi Layer Perceptron (MLP) Model
==================================

**Model Name**:  probe_ably.core.models.linear.LinearModel

.. automodule:: probe_ably.core.models.mlp
    :members:
    :special-members: __init__

Here :code:`representation_size` and :code:`n_classes` will be provided during runtime by the trainer initated from the data.
:code:`dropout`, :code:`hidden_size` and :code:`n_layers` values are static value ranges are provided in **config/params/mlp.json** file.
The :code:`probe_ably.core.utils.grid_model_factory` (See `Grid Model Factory <../utils/grid_factory.html>`_)  creates multiple models with the prescribe values for probing.

**config/params/mlp.json** is defined as follows:

.. code-block:: json

    {
        "probe_ably.core.models.mlp.MLPModel":{
        "params":[
            {
                "name":"hidden_size",
                "type":"int_range",
                "options":[
                    32,
                    1024
                ]
            },
            {
                "name":"n_layers",
                "type":"int_range",
                "options":[
                    1,
                    10
                ]
            },
            {
                "name":"dropout",
                "type":"float_range",
                "options":[
                    0.0,
                    0.5
                ]
            }
        ]
        }
    }


Here the ranges of :code:`__init__` static params is as follows:

- :code:`dropout` is of float range between 0.0 and 0.5
- :code:`n_layers` is of int range between 1 and 10
- :code:`hidden_size` is of int range between 32 and 1024




Implementing New Probing Models
*******************************

If you are to implement a new Probing Model. There are two steps

**Step 1**: Implementing model by extending the abstract Model

.. automodule:: probe_ably.core.models.abstract_model
    :members:
    :special-members: __init__

Here :code:`representation_size` and :code:`n_classes` will be provided during runtime by the trainer initated from the data.


**Step 2**: Create JSON configuration file with the ranges to create models. Refer to **config/params/mlp.json** and **config/params/linear.json** for example.



