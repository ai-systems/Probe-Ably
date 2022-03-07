import random
from typing import Dict, List
from copy import copy, deepcopy
import numpy as np
import torch
from loguru import logger
from prefect import Task
from probe_ably.metrics import AbstractIntraModelMetric
from probe_ably.utils import GridModelFactory, ProbingTask, ProbingConfig, ProbingInput
from torch.utils.data import DataLoader
from tqdm import tqdm
from colorama import Fore

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
        return_trained_model=False
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

        if return_trained_model:
            return {
                "preds_test": preds_test,
                "trained_model": best_model
            }

        else: 
            return {
                "preds_test": preds_test
                }

    def run(self, tasks: List[ProbingTask], probing_setup: ProbingConfig, thread=None, return_trained_model=False) -> Dict:
        """Runs the Probing models

        :param tasks: Data content of the models for probing.
        :type tasks: Dict
        :param probing_setup: Experiment setup for probing.
        :type probing_setup: Dict
        :return: Dictionary containing the following values:
        {int(task id) :
            "models": {
                int (model id) : {
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

        task_loop_bar = tqdm(
            tasks,
            desc=f"Task progress",
            bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.GREEN, Fore.RESET),
        )
        if thread:
            thread.task_loop_bar = task_loop_bar
        
        for id_task, content_tasks in enumerate(task_loop_bar):
            task_loop_bar.set_description(
                f"Task: {content_tasks['task_name']} progress"
            )
            output_results[id_task] = dict()
            output_results[id_task]["representations"] = dict()
            output_results[id_task]["task_name"] = content_tasks["task_name"]

            reps_loop_bar = tqdm(
                content_tasks["representations"],
                desc=f"Model progress",
                bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.BLUE, Fore.RESET),
                leave=False,
            )
            if thread:
                thread.reps_loop_bar = reps_loop_bar
            for id_model, rep_content in enumerate(reps_loop_bar):
                reps_loop_bar.set_description(
                    f"Model: {rep_content['representation_name']} progress"
                )

                output_results[id_task]["representations"][id_model] = dict()
                output_results[id_task]["representations"][id_model][
                    "representation_name"
                ] = rep_content["representation_name"]

                model_params = {
                    "representation_size": rep_content["representation_size"],
                    "n_classes": rep_content["number_of_classes"],
                }

                for id_prob_model, probe_content in enumerate(probing_setup["probing_models"]):
                    probe_model_name = probe_content["probing_model_name"]

                    probing_models = GridModelFactory.create_models(
                        probe_model_name,
                        probe_content["number_of_models"],
                        model_params,
                    )

                    output_results[id_task]["representations"][id_model][
                        probe_model_name
                    ] = dict()
                    run_number = 0
                    train_batch_size = probe_content["batch_size"] * max(1, n_gpu)

                    probes_loop_bar = tqdm(
                        probing_models,
                        desc="Probe Progress",
                        leave=False,
                        bar_format="{l_bar}%s{bar}%s{r_bar}"
                        % (Fore.YELLOW, Fore.RESET),
                    )
                    if thread:
                        thread.probes_loop_bar = probes_loop_bar
                    for probe in probes_loop_bar:
                        probes_loop_bar.set_description(
                            f"Probe: {probe_model_name} progress"
                        )
                        probe_for_model = deepcopy(probe)
                        probe_for_control = deepcopy(probe)
                        train_output = self.start_training_process(
                            train=rep_content["representation"]["train"],
                            test=rep_content["representation"]["test"],
                            dev=rep_content["representation"]["dev"],
                            train_batch_size=train_batch_size,
                            model=probe_for_model,
                            device=device,
                            num_epochs=probe_content["epochs"],
                            n_gpu=n_gpu,
                            eval_fn=intra_metric_object.calculate_metrics,
                            return_trained_model=return_trained_model
                        )

                        preds_model = train_output["preds_test"]
                        if return_trained_model:
                            trained_probe_model  = train_output["trained_model"]

                        if rep_content["default_control"]:
                            test_control_set = rep_content["control"]["train"]
                        else:
                            test_control_set = rep_content["control"]["test"]
                        preds_control = self.start_training_process(
                            train=rep_content["control"]["train"],
                            test=test_control_set,
                            dev=rep_content["control"]["dev"],
                            train_batch_size=train_batch_size,
                            model=probe_for_control,
                            device=device,
                            num_epochs=probe_content["epochs"],
                            n_gpu=n_gpu,
                            eval_fn=intra_metric_object.calculate_metrics,
                            return_trained_model=False
                        )["preds_test"]

                        output_results[id_task]["representations"][id_model][probe_model_name][
                            run_number
                        ] = {
                            "complexity": probe_for_model.get_complexity(),
                            "model": {
                                "labels": rep_content["representation"]["test"].labels,
                                "preds": preds_model,
                            },
                            "control": {
                                "labels": test_control_set.labels,
                                "preds": preds_control,
                            },
                        }
                        #TODO: adjust this for returned model
                        # if return_trained_model:
                        #     output_results[id_task]["models"][id_model][probe_model_name][
                        #         run_number
                        #     ][model]["trained_model"] =  trained_probe_model

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
                    # logger.info(f"LOSS SCALAR {loss_scalar}")
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
                    # logger.success(
                    #     f"Epoch: {epochs_trained} - Saving new model with best score: {score}"
                    # )
                    best_model = model
                    best_score = score
            epochs_trained += 1
        # logger.info("Done")
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