import click
import prefect
from dynaconf import settings
from loguru import logger
from prefect import Flow, task
from prefect.engine.flow_runner import FlowRunner
from probe_ably.core.tasks.metric_task import ProcessMetricTask
from probe_ably.core.tasks.probing import PrepareDataForProbingTask, TrainProbingTask
from probe_ably.core.tasks.utils import ReadInputTask, VisualiaztionTask

INPUT_FILE = "./tests/sample_files/test_input/multi_task_multi_model_with_control.json"
read_input_task = ReadInputTask()
prepare_data_probing = PrepareDataForProbingTask()
train_probing_task = TrainProbingTask()
process_metric_task = ProcessMetricTask()
visualization_task = VisualiaztionTask()


@click.command()
@click.option("--config_file", help="Probing Configuration File")
def run_probing(config_file):
    with Flow("Running Probe") as flow1:
        parsed_input = read_input_task(config_file)
        prepared_data = prepare_data_probing(
            parsed_input["tasks"], parsed_input["probing_setup"]
        )
        train_results = train_probing_task(prepared_data, parsed_input["probing_setup"])
        processed_results = process_metric_task(
            train_results, parsed_input["probing_setup"]
        )
        visualization_task(processed_results)
    FlowRunner(flow=flow1).run()


if __name__ == "__main__":
    run_probing()
