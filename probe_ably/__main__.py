import click
import asyncio
from uvicorn import config
from probe_ably.probing import TrainProbingTask
from probe_ably.metrics import ProcessMetricTask
from probe_ably.utils import ReadInputTask
from probe_ably.experiment_setup import ProbingExperiment

read_input_task = ReadInputTask()
train_probing_task = TrainProbingTask()
process_metric_task = ProcessMetricTask()

# class ProbingExperiment():
#     def __init__(self) -> None:
#         self.prepared_data = None
#         self.probing_setup = None

#     def from_files(self, config_file, split=False):
#         parsed_input = asyncio.run(read_input_task.run(config_file))
#         self.prepared_data = prepare_data_probing.run(
#             parsed_input["tasks"], parsed_input["probing_setup"]
#         )
#         self.probing_setup = parsed_input["probing_setup"]
    

#     def from_dataloader(self):
#         pass


#     def run(self):
#             train_results = train_probing_task.run(self.prepared_data, self.probing_setup)
#             processed_results = process_metric_task.run(
#                 train_results, self.probing_setup
#             )
#             #TODO: repair and restore visualization task
#             # visualization_task.run(processed_results)


###
# Basic functionality presented as a user interface
### 
@click.command()
@click.option("--config_file",
    help="Probing Configuration File",
    default="./tests/sample_files/test_input/multi_task_multi_model_with_control.json")
def main(config_file):
    experiment = ProbingExperiment.from_json(config_file)
    experiment.run()

if __name__ == "__main__":
    main()