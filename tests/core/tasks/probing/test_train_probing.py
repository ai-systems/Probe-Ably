import unittest
from loguru import logger
from probe_ably.core.tasks.utils import ReadInputTask
from probe_ably.core.tasks.probing import PrepareDataFromProbingTask, TrainProbingTask


class TrainProbingTest(unittest.TestCase):
    def test_train_probing(self):
        TEST_INPUT = (
            "./tests/sample_files/test_input/multi_task_multi_model_with_control.json"
        )
        read_input_task = ReadInputTask()

        output = read_input_task.run(TEST_INPUT)

        prepare_data_probing_task = PrepareDataFromProbingTask()

        dataset = prepare_data_probing_task.run(output)

        train_probing_task = TrainProbingTask()

        experiments = dict()
        train_probing_task.run(dataset, experiments)
