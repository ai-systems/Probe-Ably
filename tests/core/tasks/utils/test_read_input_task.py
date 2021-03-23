import unittest
from loguru import logger
from probe_ably.core.tasks.utils import ReadInputTask


class PrepareRicoScaTest(unittest.TestCase):
    def test_wrong_split_size(self):
        TEST_INPUT = "./tests/sample_files/test_input/wrong_split_size.json"
        read_input_task = ReadInputTask()

        self.assertRaises(SystemExit, read_input_task.run, TEST_INPUT)

    def test_multi_task_multi_model_with_control_with_setup(self):
        TEST_INPUT = (
            "./tests/sample_files/test_input/multi_task_multi_model_with_control.json"
        )
        read_input_task = ReadInputTask()

        output = read_input_task.run(TEST_INPUT)

        self.assertEquals(len(output["tasks"][0]["models"][0]["model_labels"]), 10)

    def test_multi_task_multi_model_with_control_with_no_setup(self):
        TEST_INPUT = "./tests/sample_files/test_input/multi_task_multi_model_with_control_no_setup.json"
        read_input_task = ReadInputTask()

        output = read_input_task.run(TEST_INPUT)

        self.assertEquals(output["probing_setup"]["train_size"], 0.60)

    def test_wrong_setup(self):
        TEST_INPUT = "./tests/sample_files/test_input/wrong_setup.json"
        read_input_task = ReadInputTask()

        self.assertRaises(SystemExit, read_input_task.run, TEST_INPUT)

    def test_multi_task_wrong_probing_model(self):
        TEST_INPUT = "./tests/sample_files/test_input/wrong_probing_model.json"
        read_input_task = ReadInputTask()

        # output = read_input_task.run(TEST_INPUT)

        self.assertRaises(SystemExit, read_input_task.run, TEST_INPUT)

    def test_multi_task_wrong_inter_metric(self):
        TEST_INPUT = "./tests/sample_files/test_input/wrong_inter.json"
        read_input_task = ReadInputTask()

        self.assertRaises(SystemExit, read_input_task.run, TEST_INPUT)

    def test_multi_task_wrong_intra_metric(self):
        TEST_INPUT = "./tests/sample_files/test_input/wrong_intra.json"
        read_input_task = ReadInputTask()

        # output = read_input_task.run(TEST_INPUT)

        self.assertRaises(SystemExit, read_input_task.run, TEST_INPUT)

    def test_wrong_control_size(self):
        TEST_INPUT = "./tests/sample_files/test_input/wrong_control_size.json"
        read_input_task = ReadInputTask()

        self.assertRaises(SystemExit, read_input_task.run, TEST_INPUT)

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
