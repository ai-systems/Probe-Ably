from unittest import IsolatedAsyncioTestCase
from loguru import logger
from probe_ably.utils import ReadInputTask

#TODO  convert to test for from_parsed_json 

# class PrepareProbingDataTest(IsolatedAsyncioTestCase):
#     async def test_prepare_data_probing(self):
#         TEST_INPUT = (
#             "./tests/sample_files/test_input/multi_task_multi_model_with_control.json"
#         )
#         read_input_task = ReadInputTask()

#         output = await read_input_task.run(TEST_INPUT)

#         prepare_data_probing_task = PrepareDataForProbingTask()

#         dataset = prepare_data_probing_task.run(
#             output["tasks"], output["probing_setup"]
#         )

#         total_size = (
#             dataset[0]["models"][0]["model"]["train"].__len__()
#             + dataset[0]["models"][0]["model"]["dev"].__len__()
#             + dataset[0]["models"][0]["model"]["test"].__len__()
#         )

#         original_size = len(output["tasks"][0]["models"][0]["model_vectors"])

#         model_element = dataset[0]["models"][0]["model"]["train"].__getitem__(0)[0][0]
#         control_element = dataset[0]["models"][0]["control"]["train"].__getitem__(0)[0][
#             0
#         ]

#         self.assertEqual(model_element, control_element)
#         self.assertEqual(total_size, original_size)