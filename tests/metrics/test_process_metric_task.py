import unittest

from numpy import array
from probe_ably.metrics import ProcessMetricTask


class ProcessMetricTaskTest(unittest.TestCase):
    def test_process_metric_task(self):
        metric_results = {
            0: {
                "representations": {
                    0: {
                        "representation_name": "AUX TASK 1 - MODEL 1",
                        "probe_ably.models.linear.LinearModel": {
                            0: {
                                "complexity": {"norm": 1.1320844888687134},
                                "model": {
                                    "labels": array([0, 0, 0]),
                                    "preds": array([1, 1, 0]),
                                },
                                "control": {
                                    "labels": array([0, 0, 1]),
                                    "preds": array([1, 1, 0]),
                                },
                            },
                            1: {
                                "complexity": {"norm": 1.210616946220398},
                                "model": {
                                    "labels": array([0, 0, 0]),
                                    "preds": array([0, 1, 0]),
                                },
                                "control": {
                                    "labels": array([0, 0, 1]),
                                    "preds": array([0, 1, 0]),
                                },
                            },
                        },
                        "probe_ably.models.mlp.MLPModel": {
                            0: {
                                "complexity": {"nparams": 18080},
                                "model": {
                                    "labels": array([0, 0, 0]),
                                    "preds": array([1, 1, 1]),
                                },
                                "control": {
                                    "labels": array([0, 0, 1]),
                                    "preds": array([1, 1, 1]),
                                },
                            },
                            1: {
                                "complexity": {"nparams": 613092},
                                "model": {
                                    "labels": array([0, 0, 0]),
                                    "preds": array([1, 1, 1]),
                                },
                                "control": {
                                    "labels": array([0, 0, 1]),
                                    "preds": array([1, 1, 1]),
                                },
                            },
                        },
                    },
                    1: {
                        "representation_name": "AUX TASK 1 - MODEL 2",
                        "probe_ably.models.linear.LinearModel": {
                            0: {
                                "complexity": {"norm": 1.2004743814468384},
                                "model": {
                                    "labels": array([0, 0, 0]),
                                    "preds": array([1, 0, 0]),
                                },
                                "control": {
                                    "labels": array([1, 0, 1]),
                                    "preds": array([1, 0, 0]),
                                },
                            },
                            1: {
                                "complexity": {"norm": 1.209789514541626},
                                "model": {
                                    "labels": array([0, 0, 0]),
                                    "preds": array([1, 0, 0]),
                                },
                                "control": {
                                    "labels": array([1, 0, 1]),
                                    "preds": array([1, 0, 0]),
                                },
                            },
                        },
                        "probe_ably.models.mlp.MLPModel": {
                            0: {
                                "complexity": {"nparams": 3536},
                                "model": {
                                    "labels": array([0, 0, 0]),
                                    "preds": array([0, 0, 0]),
                                },
                                "control": {
                                    "labels": array([1, 0, 1]),
                                    "preds": array([0, 1, 0]),
                                },
                            },
                            1: {
                                "complexity": {"nparams": 337364},
                                "model": {
                                    "labels": array([0, 0, 0]),
                                    "preds": array([0, 0, 0]),
                                },
                                "control": {
                                    "labels": array([1, 0, 1]),
                                    "preds": array([0, 0, 0]),
                                },
                            },
                        },
                    },
                },
                "task_name": "AUX TASK 1",
            },
            1: {
                "representations": {
                    0: {
                        "representation_name": "AUX TASK 2 - MODEL 1",
                        "probe_ably.models.linear.LinearModel": {
                            0: {
                                "complexity": {"norm": 1.0756611824035645},
                                "model": {
                                    "labels": array([1, 1, 1, 1, 0, 0, 1, 1]),
                                    "preds": array([0, 0, 1, 0, 1, 0, 0, 1]),
                                },
                                "control": {
                                    "labels": array([0, 0, 1, 0, 0, 0, 1, 1]),
                                    "preds": array([0, 0, 1, 0, 1, 0, 0, 1]),
                                },
                            },
                            1: {
                                "complexity": {"norm": 1.127833604812622},
                                "model": {
                                    "labels": array([1, 1, 1, 1, 0, 0, 1, 1]),
                                    "preds": array([0, 1, 0, 0, 0, 0, 1, 0]),
                                },
                                "control": {
                                    "labels": array([0, 0, 1, 0, 0, 0, 1, 1]),
                                    "preds": array([0, 1, 0, 0, 0, 1, 1, 0]),
                                },
                            },
                        },
                        "probe_ably.models.mlp.MLPModel": {
                            0: {
                                "complexity": {"nparams": 32937},
                                "model": {
                                    "labels": array([1, 1, 1, 1, 0, 0, 1, 1]),
                                    "preds": array([1, 1, 1, 1, 1, 1, 1, 1]),
                                },
                                "control": {
                                    "labels": array([0, 0, 1, 0, 0, 0, 1, 1]),
                                    "preds": array([0, 1, 1, 1, 0, 1, 1, 1]),
                                },
                            },
                            1: {
                                "complexity": {"nparams": 26263},
                                "model": {
                                    "labels": array([1, 1, 1, 1, 0, 0, 1, 1]),
                                    "preds": array([0, 1, 0, 0, 1, 1, 1, 0]),
                                },
                                "control": {
                                    "labels": array([0, 0, 1, 0, 0, 0, 1, 1]),
                                    "preds": array([0, 1, 0, 0, 1, 1, 1, 0]),
                                },
                            },
                        },
                    },
                    1: {
                        "representation_name": "AUX TASK 2 - MODEL 2",
                        "probe_ably.models.linear.LinearModel": {
                            0: {
                                "complexity": {"norm": 1.1543824672698975},
                                "model": {
                                    "labels": array([1, 0, 0, 0, 1, 1, 1, 0]),
                                    "preds": array([1, 0, 0, 0, 1, 1, 1, 0]),
                                },
                                "control": {
                                    "labels": array([1, 1, 1, 1, 0, 1, 1, 0]),
                                    "preds": array([1, 0, 0, 1, 1, 1, 1, 0]),
                                },
                            },
                            1: {
                                "complexity": {"norm": 1.0753788948059082},
                                "model": {
                                    "labels": array([1, 0, 0, 0, 1, 1, 1, 0]),
                                    "preds": array([1, 0, 1, 1, 0, 0, 0, 1]),
                                },
                                "control": {
                                    "labels": array([1, 1, 1, 1, 0, 1, 1, 0]),
                                    "preds": array([1, 0, 1, 1, 0, 0, 0, 1]),
                                },
                            },
                        },
                        "probe_ably.models.mlp.MLPModel": {
                            0: {
                                "complexity": {"nparams": 291363},
                                "model": {
                                    "labels": array([1, 0, 0, 0, 1, 1, 1, 0]),
                                    "preds": array([0, 1, 1, 0, 0, 1, 0, 0]),
                                },
                                "control": {
                                    "labels": array([1, 1, 1, 1, 0, 1, 1, 0]),
                                    "preds": array([1, 1, 1, 0, 0, 1, 0, 0]),
                                },
                            },
                            1: {
                                "complexity": {"nparams": 430130},
                                "model": {
                                    "labels": array([1, 0, 0, 0, 1, 1, 1, 0]),
                                    "preds": array([1, 0, 1, 0, 1, 1, 0, 1]),
                                },
                                "control": {
                                    "labels": array([1, 1, 1, 1, 0, 1, 1, 0]),
                                    "preds": array([1, 1, 1, 1, 1, 1, 1, 1]),
                                },
                            },
                        },
                    },
                    2: {
                        "representation_name": "AUX TASK 2 - MODEL 3",
                        "probe_ably.models.linear.LinearModel": {
                            0: {
                                "complexity": {"norm": 1.1083829402923584},
                                "model": {
                                    "labels": array([0, 0, 1, 0, 0, 0, 0, 0]),
                                    "preds": array([0, 1, 1, 1, 1, 0, 1, 1]),
                                },
                                "control": {
                                    "labels": array([0, 0, 0, 0, 0, 1, 0, 0]),
                                    "preds": array([0, 1, 1, 1, 1, 0, 1, 1]),
                                },
                            },
                            1: {
                                "complexity": {"norm": 1.1510838270187378},
                                "model": {
                                    "labels": array([0, 0, 1, 0, 0, 0, 0, 0]),
                                    "preds": array([0, 0, 1, 1, 0, 1, 0, 1]),
                                },
                                "control": {
                                    "labels": array([0, 0, 0, 0, 0, 1, 0, 0]),
                                    "preds": array([0, 0, 1, 1, 0, 1, 0, 1]),
                                },
                            },
                        },
                        "probe_ably.models.mlp.MLPModel": {
                            0: {
                                "complexity": {"nparams": 303989},
                                "model": {
                                    "labels": array([0, 0, 1, 0, 0, 0, 0, 0]),
                                    "preds": array([1, 1, 1, 1, 1, 1, 1, 1]),
                                },
                                "control": {
                                    "labels": array([0, 0, 0, 0, 0, 1, 0, 0]),
                                    "preds": array([1, 1, 1, 0, 1, 1, 1, 1]),
                                },
                            },
                            1: {
                                "complexity": {"nparams": 32381},
                                "model": {
                                    "labels": array([0, 0, 1, 0, 0, 0, 0, 0]),
                                    "preds": array([0, 1, 0, 0, 0, 0, 0, 1]),
                                },
                                "control": {
                                    "labels": array([0, 0, 0, 0, 0, 1, 0, 0]),
                                    "preds": array([0, 1, 0, 0, 0, 0, 0, 1]),
                                },
                            },
                        },
                    },
                },
                "task_name": "AUX TASK 2",
            },
        }

        print(metric_results)
        process_metric_task = ProcessMetricTask()

        processed_data = process_metric_task.run(
            metric_results,
            {
                "intra_metric": "probe_ably.metrics.accuracy.AccuracyMetric",
                "inter_metric": "probe_ably.metrics.selectivity.SelectivityMetric",
            },
        )
        self.assertEqual(len(processed_data), 2)
        self.assertEqual(processed_data[0]["name"], "AUX TASK 1")
        self.assertEqual(processed_data[1]["name"], "AUX TASK 2")
        self.assertEqual(len(processed_data[0]["probings"]), 2)
        self.assertNotEqual(
            processed_data[0]["probings"][0], processed_data[0]["probings"][1]
        )
        other = "norm"
        for data in processed_data[0]["probings"][0]["probing_results"]:
            self.assertEqual(len(data["chart_data"]), 2)
            try:
                self.assertEqual(data["x_axis"], "nparams")
            except:
                self.assertEqual(data["x_axis"], "norm")
                other = "nparams"
        for data in processed_data[0]["probings"][1]["probing_results"]:
            self.assertEqual(data["x_axis"], other)

        for data in processed_data[1]["probings"][0]["probing_results"]:
            self.assertEqual(len(data["chart_data"]), 3)
