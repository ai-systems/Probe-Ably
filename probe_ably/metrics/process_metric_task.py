import random
from collections import defaultdict
from typing import Dict

import numpy as np
from loguru import logger
from prefect import Task
from probe_ably.metrics.abstract_inter_model_metric import AbstractInterModelMetric
from probe_ably.metrics.abstract_intra_model_metric import AbstractIntraModelMetric
from tqdm import tqdm


class ProcessMetricTask(Task):
    def run(
        self, train_results: Dict[str, Dict], probing_configuration: Dict[str, Dict]
    ):
        logger.info("Calculating and processing metrics")
        intra_metric = AbstractIntraModelMetric.subclasses[
            probing_configuration["intra_metric"]
        ]()
        inter_metric = AbstractInterModelMetric.subclasses[
            probing_configuration["inter_metric"]
        ]()
        inter_eval_metric, inter_eval_name = (
            inter_metric,
            inter_metric.metric_name(),
        )
        intra_eval_metric, intra_eval_name = intra_metric, intra_metric.metric_name()

        processed_aux_tasks = []
        probing_models, reps, x_axis_data, y_axis_data = set(), set(), set(), set()
        for task_id, task_data in tqdm(train_results.items(), "Processing task data"):
            processed_task = {}
            processed_task["id"] = task_id
            processed_task["name"] = task_data["task_name"]
            processed_task["probings"] = defaultdict(lambda: [])
            for _, rep_data in task_data["models"].items():
                rep_name = rep_data["representation_name"]
                for probing_model, probing_data in rep_data.items():
                    if probing_model != "representation_name":
                        for p_data in probing_data.values():
                            for cplx_key, cplx_data in p_data["complexity"].items():
                                model_gold, model_preds = (
                                    p_data["model"]["labels"],
                                    p_data["model"]["preds"],
                                )
                                control_gold, control_preds = (
                                    p_data["control"]["labels"],
                                    p_data["control"]["preds"],
                                )
                                intra_score = intra_eval_metric.calculate_metrics(
                                    targets=model_gold,
                                    predicitons=model_preds,
                                )
                                inter_score = inter_eval_metric.calculate_metrics(
                                    targets1=model_gold,
                                    targets2=control_gold,
                                    predicitons1=model_preds,
                                    predicitons2=control_preds,
                                )
                                processed_task["probings"][
                                    (
                                        probing_model,
                                        rep_name,
                                        cplx_key,
                                        inter_eval_name,
                                    )
                                ].append(
                                    {
                                        "y": round(inter_score, 2),
                                        "x": round(cplx_data, 2),
                                    }
                                )

                                probing_models.add(probing_model)
                                reps.add(rep_name)
                                x_axis_data.add(cplx_key)
                                y_axis_data.add(inter_eval_name)
                                y_axis_data.add(intra_eval_name)

                                processed_task["probings"][
                                    (
                                        probing_model,
                                        rep_name,
                                        cplx_key,
                                        intra_eval_name,
                                    )
                                ].append(
                                    {
                                        "y": round(intra_score, 2),
                                        "x": round(cplx_data, 2),
                                    }
                                )
            processed_aux_tasks.append(processed_task)

        visual_data_tasks = []
        for processed_task in processed_aux_tasks:
            visual_data_task = {}
            visual_data_task["id"] = processed_task["id"]
            visual_data_task["name"] = processed_task["name"]
            visual_data_task["probings"] = []
            for probing_model in probing_models:
                probing_data = {}
                probing_data["representation_name"] = probing_model
                probing_data["probing_results"] = []
                for x_axis in x_axis_data:
                    for y_axis in y_axis_data:
                        rep_data = {}
                        for rep_name in reps:
                            if (
                                len(
                                    processed_task["probings"][
                                        (probing_model, rep_name, x_axis, y_axis)
                                    ]
                                )
                                > 0
                            ):
                                m_data = {
                                    "id": rep_name,
                                    "color": f"hsl({random.randint(1,360)}, {int(random.randint(1,9))*10}%, {int(random.randint(1,9))*10}%)",
                                }
                                m_data["data"] = []
                                x, y = [], []
                                for point in processed_task["probings"][
                                    (probing_model, rep_name, x_axis, y_axis)
                                ]:
                                    x.append(point["x"])
                                    y.append(point["y"])
                                    # m_data["data"].append(point)
                                for index in np.argsort(x):
                                    m_data["data"].append(
                                        {"x": x[index], "y": y[index]}
                                    )

                                if "chart_data" not in rep_data:
                                    rep_data["x_axis"] = x_axis
                                    rep_data["y_axis"] = y_axis
                                    rep_data["chart_data"] = []
                                rep_data["chart_data"].append(m_data)
                        if len(rep_data) > 0:
                            probing_data["probing_results"].append(rep_data)
                visual_data_task["probings"].append(probing_data)
            visual_data_tasks.append(visual_data_task)
        return visual_data_tasks