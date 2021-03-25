# Quick Start

## Representation File

The representation file that you are going to test in expected to be a tab seperated `tsv` file with one column for each dimension, separated by \t, last column is assumed to be the label.

*Example*:
```
-868.2718787247023	-430.12670399541776	641.1996396389518	...	-695.8058457450846	-413.83211646514155	3.313256558177727	0
31.32994666249101	554.0715987660915	-436.32803493627034	...	-988.659113623684	162.09461427769747	643.9950838538996	1
```

## Configuration File

Following is a sample format of the probing configuration file:

```
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
      {
         "task_name":"NER Tagging",
         "models":[
            {
               "model_name":"Roberta-Base",
               "file_location":"./representations_folder/roberta_base.tsv"
            },
            {
               "model_name":"BERT-Base",
               "file_location":"./representations_folder/bert_base.tsv"
            },
            {
               "model_name":"SBERT-Base-NLI",
               "file_location":"./representations_folder/sbert_base_nli.tsv"
            }
         ]
      }
   ]
}
```

In this configuration file.
- `task_name`: The name of the task you are planning to probe. This name will be reflected with tabs in the visualization service
- `model_name`: The name of the models you are probing. Each task can have multiple models
- `file_location`: The location of the representation file for the respective model.
- `control_location`: The location file of the representations. Contains only the labels for the respective index int the representation file. If this file location is not provided, we genearate the control labels randomly


## Launching Your First Probe

`python -m probe_ably.core.flows.run_probing --config_file <config_file_path>`

At the end of the probe you will be directed or prompted to visit the following address: `http://127.0.0.1:8031/` where you can see the visualzation output.

By default probing will run the `Linear Model` and `MLP Model` with Accuracy and Selectivity as the default metrics. If you want to change the run configurations of these models see [Probing Configurations](/advanced/configurations.md).





