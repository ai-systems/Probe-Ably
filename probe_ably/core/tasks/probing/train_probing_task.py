from overrides import overrides
from prefect import Task
from loguru import logger
from typing import Dict
import torch
from torch.utils.data import DataLoader
import random
import numpy as np
from probe_ably.core.utils import GridModelFactory
from probe_ably.core.models import LinearModel
from tqdm import tqdm, trange
from sklearn.metrics import accuracy_score
from probe_ably.core.metrics import AbstractIntraModelMetric


class TrainProbingTask(Task):
    def __init__(self, **kwargs):
        self.per_gpu_batch_size = kwargs.get("per_gpu_batch_size", 2)
        self.cuda = kwargs.pop("cuda", True)
        self.num_train_epochs = kwargs.get("num_train_epochs", 5)
        self.logging_steps = kwargs.get("logging_steps", 5)
        self.probing_model_names = [
            "probe_ably.core.models.linear.LinearModel",
            "probe_ably.core.models.mlp.MLPModel",
        ]
        self.number_of_probing_models = 2
        super(TrainProbingTask, self).__init__(**kwargs)

    def set_seed(self, n_gpu, seed=42):
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if n_gpu > 0:
            torch.cuda.manual_seed_all(seed)

    def start_training_process(
        self,
        train_dataloader,
        test_dataloader,
        dev_dataloader,
        train_batch_size,
        model,
        device,
        n_gpu,
        eval_fn,
    ):
        outputs = {}
        logger.info("Running train mode")
        model = model.to(device)
        if n_gpu > 1:
            model = torch.nn.DataParallel(model)
        best_model = self.train(
            model,
            train_dataloader,
            dev_dataloader,
            device,
            n_gpu,
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
    def run(self, tasks: Dict, experiments: Dict, probing_setup: Dict):
        """[summary]

        Args:
            tasks ([Dict]): {task_id: {"task_name": str,
                        "models": {model_id: {
                                                "model_name": str,
                                                "model": { "train": TorchDataset, "dev": TorchDataset, "test": TorchDataset }
                                                "control": { "train": TorchDataset, "dev": TorchDataset, "test": TorchDataset }
                                            }
                                }
                        }
                }
            experiments ([type]): [description]
        """

        logger.debug("Starting the Probing Training Task")
        torch.cuda.empty_cache()
        device = torch.device(
            "cuda" if torch.cuda.is_available() and self.cuda else "cpu"
        )

        n_gpu = torch.cuda.device_count()
        self.set_seed(n_gpu)
        self.logger.info(f"GPUs used {n_gpu}")

        train_batch_size = self.per_gpu_batch_size * max(1, n_gpu)

        n_gpu = torch.cuda.device_count()
        output_results = dict()
        intra_metric_class = AbstractIntraModelMetric.subclasses[
            probing_setup["intra_metric"]
        ]
        intra_metric_object = intra_metric_class()
        for id_task, content_tasks in tasks.items():
            output_results[id_task] = dict()
            output_results[id_task]["models"] = dict()
            output_results[id_task]["task_name"] = content_tasks["task_name"]
            for id_model, model_content in content_tasks["models"].items():
                output_results[id_task]["models"][id_model] = dict()
                output_results[id_task]["models"][id_model][
                    "model_name"
                ] = model_content["model_name"]
                model_params = {
                    "representation_size": model_content["representation_size"],
                    "n_classes": model_content["number_of_classes"],
                }

                model_train_dataloader = DataLoader(
                    model_content["model"]["train"],
                    batch_size=train_batch_size,
                    shuffle=True,
                )
                model_dev_dataloader = DataLoader(
                    model_content["model"]["dev"],
                    batch_size=train_batch_size,
                    shuffle=False,
                )
                model_test_dataloader = DataLoader(
                    model_content["model"]["test"],
                    batch_size=train_batch_size,
                    shuffle=False,
                )

                control_train_dataloader = DataLoader(
                    model_content["control"]["train"],
                    batch_size=train_batch_size,
                    shuffle=True,
                )
                control_dev_dataloader = DataLoader(
                    model_content["control"]["dev"],
                    batch_size=train_batch_size,
                    shuffle=False,
                )
                control_test_dataloader = DataLoader(
                    model_content["control"]["test"],
                    batch_size=train_batch_size,
                    shuffle=False,
                )

                for name in self.probing_model_names:
                    probing_models = GridModelFactory.create_models(
                        name, self.number_of_probing_models, model_params
                    )
                    output_results[id_task]["models"][id_model][name] = dict()
                    run_number = 0
                    for probe in probing_models:
                        preds_model = self.start_training_process(
                            model_train_dataloader,
                            model_test_dataloader,
                            model_dev_dataloader,
                            train_batch_size,
                            probe,
                            device,
                            n_gpu,
                            eval_fn=intra_metric_object.calculate_metrics,
                        )

                        preds_control = self.start_training_process(
                            control_train_dataloader,
                            control_test_dataloader,
                            control_dev_dataloader,
                            train_batch_size,
                            probe,
                            device,
                            n_gpu,
                            eval_fn=accuracy_score,
                        )
                        output_results[id_task]["models"][id_model][name][
                            run_number
                        ] = {
                            "complexity": probe.get_complexity(),
                            "model": {
                                "labels": model_content["model"]["test"].labels,
                                "preds": preds_model,
                            },
                            "control": {
                                "labels": model_content["control"]["test"].labels,
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
        eval_fn,
    ):
        best_score = -1.0

        optimizer = torch.optim.Adam(model.parameters())

        global_step = 0
        epochs_trained = 0

        tr_loss, logging_loss = 0.0, 0.0
        model.zero_grad()
        train_iterator = trange(
            epochs_trained,
            int(self.num_train_epochs),
            desc="Epoch",
        )

        for epoch in train_iterator:
            epoch_iterator = tqdm(train_dataloader, desc="Iteration")
            for step, batch in enumerate(epoch_iterator):
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

                    epoch_iterator.set_description(f"Loss :{loss_scalar}")

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
                    logger.success(f"Saving new model with best F1-score: {score}")
                    best_model = model
                    best_score = score

        return best_model

    def eval(self, model, dataloader, device, n_gpu, eval_fn):
        if n_gpu > 1 and not isinstance(model, torch.nn.DataParallel):
            model = torch.nn.DataParallel(model)
        eval_loss = 0.0
        nb_eval_steps = 0
        preds = None

        for batch in tqdm(dataloader, desc="Evaluating"):
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
        logger.info(f"Score:{score}")

        return score, preds
