import click
import prefect
from dynaconf import settings
from loguru import logger
from prefect import Flow
from prefect.engine.flow_runner import FlowRunner
from probe_ably.core.tasks.probing import TrainProbingTask
from probe_ably.core.tasks.metric_task import ProcessMetricTask

INPUT_FILE = "./tests/sample_files/test_input/multi_task_multi_model_with_control.json"
train_probing_task = TrainProbingTask()
process_metric_task = ProcessMetricTask()

def probe_from_dataloaders(config_dict, prepared_data):
    with Flow("Running Probe") as flow1:
        train_results = train_probing_task(prepared_data, config_dict["probing_setup"])
        processed_results = process_metric_task(
            train_results, config_dict["probing_setup"]
        )
    FlowRunner(flow=flow1).run