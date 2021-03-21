import unittest
from loguru import logger
from probe_ably.core.tasks.utils import ReadInputTask


class PrepareRicoScaTest(unittest.TestCase):
    def test_multi_task_multi_model_with_control(self):
        TEST_INPUT = (
            "./tests/sample_files/test_input/multi_task_multi_model_with_control.json"
        )
        read_input_task = ReadInputTask()

        read_input_task.run(TEST_INPUT)

    def test_missing_key(self):

        TEST_INPUT_1 = "./tests/sample_files/test_input/missing_tasks_key.json"
        read_input_task = ReadInputTask()

        self.assertRaises(SystemExit, read_input_task.run, TEST_INPUT_1)

    def test_wrong_key_name(self):

        TEST_INPUT_2 = "./tests/sample_files/test_input/wrong_template_format.json"
        read_input_task = ReadInputTask()

        self.assertRaises(SystemExit, read_input_task.run, TEST_INPUT_2)

    def test_file_does_not_exist(self):
        TEST_INPUT = "./this/does/not/exist"
        read_input_task = ReadInputTask()
        self.assertRaises(SystemExit, read_input_task.run, TEST_INPUT)

    def test_wrong_json_format(self):
        TEST_INPUT = "./tests/sample_files/test_input/problematic_json_file.json"
        read_input_task = ReadInputTask()
        self.assertRaises(SystemExit, read_input_task.run, TEST_INPUT)
