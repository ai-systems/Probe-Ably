# Probing Configurations

The document presented in the Quick Start link is the basic configuration structure expected by the framework. The configuration file is then extend by default with the following data:

```
{
   "train_size":0.6,
   "dev_size":0.2,
   "test_size":0.2,
   "intra_metric":"probe_ably.core.metrics.accuracy.AccuracyMetric",
   "inter_metric":"probe_ably.core.metrics.selectivity.SelectivityMetric",
   "probing_models":{
      "0":{
         "probing_model_name":"probe_ably.core.models.linear.LinearModel",
         "batch_size":32,
         "epochs":25,
         "number_of_models":50
      },
      "1":{
         "probing_model_name":"probe_ably.core.models.mlp.MLPModel",
         "batch_size":32,
         "epochs":25,
         "number_of_models":50
      }
   }
}
```

If you want to customize your probing you can extend your configuration file with this data as following:

```
``
{
   "tasks":[
      {
         "task_name":"POS Tagging",
         "models":[
            {
               "model_name":"BERT-Large",
               "file_location":"./representations_folder/bert_large.tsv",
               "control_location":"./representations_folder/bert_large_control.tsv"
            },
            {
               "model_name":"Roberta-Large",
               "file_location":"./representations_folder/roberta_large.tsv",
               "control_location":"./representations_folder/roberta_large_control.tsv"
            }
         ]
      },
   ],
   "probing_setup":{
      "train_size":0.50,
      "dev_size":0.25,
      "test_size":0.25,
      "intra_metric":"probe_ably.core.metrics.accuracy.AccuracyMetric",
      "inter_metric":"probe_ably.core.metrics.selectivity.SelectivityMetric",
      "probing_models":[
         {
            "probing_model_name":"probe_ably.core.models.linear.LinearModel",
            "batch_size":5,
            "epochs":10,
            "number_of_models":5
         },
         {
            "probing_model_name":"probe_ably.core.models.mlp.MLPModel",
            "batch_size":5,
            "epochs":20,
            "number_of_models":10
         }
      ]
   }
}
```

In this configuration file:
- `train_size`, `dev_size`, `test_size` are the ratio splting of the provided dataset. 
-  `intra_metric`: Denotes the inter model metric used to select the best probing model in the auxiliary task and also part of probing ouput. For further details see [Probing Intra Model Metrics](intra_metrics.html).
-  `inter_metric`: Denotes the intra model metric used to compare the control task and auxiliary task performance. For further details see [Probing Inter Model Metrics](inter_metrics.html).
- `probing_models`: Denotes the probing models used and their repsective configurations. Further details regarding the probing models and how to add new models see [Probing Models](models.md)
