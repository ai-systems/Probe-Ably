import random
from typing import Dict, List
from copy import copy, deepcopy
import numpy as np
import torch
from loguru import logger
from overrides import overrides
from prefect import Task
from probe_ably.core.metrics import AbstractIntraModelMetric
from probe_ably.core.models import LinearModel
from probe_ably.core.utils import GridModelFactory
from sklearn.metrics import accuracy_score
from torch.utils.data import DataLoader
from tqdm import tqdm, trange
from colorama import Fore
import threading


class TrainProbingTask(Task):
    def __init__(self, **kwargs):
        self.cuda = kwargs.pop("cuda", True)
        self.logging_steps = kwargs.get("logging_steps", 5)
        super(TrainProbingTask, self).__init__(**kwargs)

    def set_seed(self, n_gpu, seed=42):
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if n_gpu > 0:
            torch.cuda.manual_seed_all(seed)

    def start_training_process(
        self,
        train,
        test,
        dev,
        train_batch_size,
        model,
        device,
        n_gpu,
        num_epochs,
        eval_fn,
    ):
        outputs = {}
        # logger.info("Running train mode")
        train_dataloader = DataLoader(
            train,
            batch_size=train_batch_size,
            shuffle=True,
        )
        dev_dataloader = DataLoader(
            dev,
            batch_size=train_batch_size,
            shuffle=False,
        )
        test_dataloader = DataLoader(
            test,
            batch_size=train_batch_size,
            shuffle=False,
        )

        model = model.to(device)
        if n_gpu > 1:
            model = torch.nn.DataParallel(model)
        best_model = self.train(
            model,
            train_dataloader,
            dev_dataloader,
            device,
            n_gpu,
            num_epochs,
            eval_fn,
        )

        score_test, preds_test = self.eval(
            best_model,
            test_dataloader,
            device,
            n_gpu,
            eval_fn,
        )

        return preds_test

    @overrides
    def run(self, tasks: Dict, probing_setup: Dict, thread: threading.Thread) -> Dict:
        """Runs the Probing models

        :param tasks: Data content of the models for probing.
        :type tasks: Dict
        :param probing_setup: Experiment setup for probing.
        :type probing_setup: Dict
        :return: Dictionary containing the following values:
        {int(task id) :
            "models": {
                int(model id) : {
                    str (name of probing model) : {
                        int (run number) : {
                            "complexity": {
                                str (name of metric): float (value for the complexity)
                            }
                            "model" : {
                                "labels": array (original labels for the auxiliary task)
                                "preds": array (predicted labels for the auxiliary task)
                            }
                            "control": {
                                "labels": array (original labels for the control task)
                                "preds": array (predicted labels for the control task)

                        }
                    }
                }
            }
        }

        :rtype: Dict
        """

        logger.debug("Starting the Probing Training Task")
        torch.cuda.empty_cache()
        device = torch.device(
            "cuda" if torch.cuda.is_available() and self.cuda else "cpu"
        )

        n_gpu = torch.cuda.device_count()
        self.set_seed(n_gpu)
        self.logger.info(f"GPUs used {n_gpu}")

        output_results = dict()
        intra_metric_class = AbstractIntraModelMetric.subclasses[
            probing_setup["intra_metric"]
        ]
        intra_metric_object = intra_metric_class()

        thread.task_loop_bar = tqdm(
            tasks.items(),
            desc=f"Task progress",
            bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET),
        )

        for id_task, content_tasks in thread.task_loop_bar:

            thread.task_loop_bar.set_description(
                f"Task: {content_tasks['task_name']} progress"
            )
            output_results[id_task] = dict()
            output_results[id_task]["models"] = dict()
            output_results[id_task]["task_name"] = content_tasks["task_name"]
            thread.model_loop_bar = tqdm(
                content_tasks["models"].items(),
                desc=f"Model progress",
                bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.BLUE, Fore.RESET),
                leave=False,
            )
            for id_model, model_content in thread.model_loop_bar:
                thread.model_loop_bar.set_description(
                    f"Model: {model_content['model_name']} progress"
                )
                output_results[id_task]["models"][id_model] = dict()
                output_results[id_task]["models"][id_model][
                    "model_name"
                ] = model_content["model_name"]

                model_params = {
                    "representation_size": model_content["representation_size"],
                    "n_classes": model_content["number_of_classes"],
                }

                for id_prob_model, probe_content in probing_setup[
                    "probing_models"
                ].items():
                    probe_model_name = probe_content["probing_model_name"]

                    probing_models = GridModelFactory.create_models(
                        probe_model_name,
                        probe_content["number_of_models"],
                        model_params,
                    )

                    output_results[id_task]["models"][id_model][
                        probe_model_name
                    ] = dict()
                    run_number = 0
                    train_batch_size = probe_content["batch_size"] * max(1, n_gpu)

                    thread.probes_loop_bar = tqdm(
                        probing_models,
                        desc="Probe Progress",
                        leave=False,
                        bar_format="{l_bar}%s{bar}%s{r_bar}"
                        % (Fore.YELLOW, Fore.RESET),
                    )
                    for probe in thread.probes_loop_bar:
                        thread.probes_loop_bar.set_description(
                            f"Probe: {probe_model_name} progress"
                        )
                        probe_for_model = deepcopy(probe)
                        probe_for_control = deepcopy(probe)
                        preds_model = self.start_training_process(
                            train=model_content["model"]["train"],
                            test=model_content["model"]["test"],
                            dev=model_content["model"]["dev"],
                            train_batch_size=train_batch_size,
                            model=probe_for_model,
                            device=device,
                            num_epochs=probe_content["epochs"],
                            n_gpu=n_gpu,
                            eval_fn=intra_metric_object.calculate_metrics,
                        )

                        if model_content["default_control"]:
                            test_control_set = model_content["control"]["train"]
                        else:
                            test_control_set = model_content["control"]["test"]
                        preds_control = self.start_training_process(
                            train=model_content["control"]["train"],
                            test=test_control_set,
                            dev=model_content["control"]["dev"],
                            train_batch_size=train_batch_size,
                            model=probe_for_control,
                            device=device,
                            num_epochs=probe_content["epochs"],
                            n_gpu=n_gpu,
                            eval_fn=intra_metric_object.calculate_metrics,
                        )
                        output_results[id_task]["models"][id_model][probe_model_name][
                            run_number
                        ] = {
                            "complexity": probe_for_model.get_complexity(),
                            "model": {
                                "labels": model_content["model"]["test"].labels,
                                "preds": preds_model,
                            },
                            "control": {
                                "labels": test_control_set.labels,
                                "preds": preds_control,
                            },
                        }
                        run_number += 1
        return output_results

    def train(
        self,
        model,
        train_dataloader,
        dev_dataloader,
        device,
        n_gpu,
        num_epochs,
        eval_fn,
    ):
        best_score = -1.0

        optimizer = torch.optim.Adam(model.parameters())

        global_step = 0
        epochs_trained = 0

        tr_loss, logging_loss = 0.0, 0.0
        model.zero_grad()
        train_iterator = range(
            epochs_trained,
            int(num_epochs),
        )

        for epoch in train_iterator:
            # epoch_iterator = tqdm(train_dataloader, desc="Iteration")
            for step, batch in enumerate(train_dataloader):
                model.train()
                batch = tuple(t.to(device) for t in batch)

                input_model = {
                    "representation": batch[0],
                    "labels": batch[1],
                }

                output = model(**input_model)

                loss = output["loss"]

                if n_gpu > 1:
                    loss = (
                        loss.mean()
                    )  # mean() to average on multi-gpu parallel training

                loss.backward()

                tr_loss += loss.item()

                optimizer.step()
                model.zero_grad()
                global_step += 1

                if self.logging_steps > 0 and global_step % self.logging_steps == 0:
                    loss_scalar = (tr_loss - logging_loss) / self.logging_steps

                    # epoch_iterator.set_description(f"Loss :{loss_scalar}")

                    logging_loss = tr_loss

            score, _ = self.eval(
                model,
                dev_dataloader,
                device,
                n_gpu,
                eval_fn,
            )

            with torch.no_grad():
                if score > best_score:
                    # logger.success(f"Saving new model with best score: {score}")
                    best_model = model
                    best_score = score

        return best_model

    def eval(self, model, dataloader, device, n_gpu, eval_fn):
        if n_gpu > 1 and not isinstance(model, torch.nn.DataParallel):
            model = torch.nn.DataParallel(model)
        eval_loss = 0.0
        nb_eval_steps = 0
        preds = None

        for batch in dataloader:
            model.eval()
            batch = tuple(t.to(device) for t in batch)

            with torch.no_grad():
                input_model = {
                    "representation": batch[0],
                    "labels": batch[1],
                }

                output = model(**input_model)
            nb_eval_steps += 1
            if preds is None:
                preds = output["preds"].detach().cpu().numpy()
                out_label_ids = input_model["labels"].detach().cpu().numpy()

            else:

                preds = np.append(preds, output["preds"].detach().cpu().numpy(), axis=0)

                out_label_ids = np.append(
                    out_label_ids, input_model["labels"].detach().cpu().numpy(), axis=0
                )

        eval_loss = eval_loss / nb_eval_steps

        score = eval_fn(preds, out_label_ids)
        # logger.info(f"Score:{score}")

        return score, preds
