import click
from probe_ably import ProbingExperiment

@click.command()
@click.option("--config_file",
    help="Probing Configuration File",
    default="./tests/sample_files/test_input/multi_task_multi_model_with_control.json")
def main(config_file):
    experiment = ProbingExperiment.from_json(config_file)
    experiment.run()

if __name__ == "__main__":
    main()