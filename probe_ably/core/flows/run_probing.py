import argparse

import prefect
from dynaconf import settings
from loguru import logger
from prefect import Flow, tags, task
from prefect.engine.flow_runner import FlowRunner
from prefect.engine.results import LocalResult
from probe_ably.core.tasks.metric_task import ProcessMetricTask
from probe_ably.core.tasks.probing import PrepareDataForProbingTask, TrainProbingTask
from probe_ably.core.tasks.utils import ReadInputTask, VisualiaztionTask

INPUT_FILE = "examples/bp_config.json"
read_input_task = ReadInputTask()
prepare_data_probing = PrepareDataForProbingTask()
train_probing_task = TrainProbingTask()
process_metric_task = ProcessMetricTask()
visualization_task = VisualiaztionTask()

with Flow("Running Probe") as flow1:
    parsed_input = read_input_task(INPUT_FILE)
    prepared_data = prepare_data_probing(parsed_input["tasks"])
    train_results = train_probing_task(prepared_data, parsed_input["probing_setup"])
    processed_results = process_metric_task(
        train_results, parsed_input["probing_setup"]
    )
    visualization_task(processed_results)


FlowRunner(flow=flow1).run()
