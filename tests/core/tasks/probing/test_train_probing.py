from unittest import IsolatedAsyncioTestCase
from loguru import logger
from probe_ably.core.tasks.utils import ReadInputTask
from probe_ably.core.tasks.probing import PrepareDataForProbingTask, TrainProbingTask


class TrainProbingTest(IsolatedAsyncioTestCase):
    async def test_train_probing(self):
        TEST_INPUT = (
            "./tests/sample_files/test_input/multi_task_multi_model_with_control.json"
        )
        read_input_task = ReadInputTask()

        output = await read_input_task.run(TEST_INPUT)

        prepare_data_probing_task = PrepareDataForProbingTask()

        dataset = prepare_data_probing_task.run(
            output["tasks"], output["probing_setup"]
        )

        train_probing_task = TrainProbingTask()

        probing_output = train_probing_task.run(dataset, output["probing_setup"])
