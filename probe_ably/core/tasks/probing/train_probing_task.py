from overrides import overrides
from prefect import Task
from loguru import logger
from typing import Dict
import torch
from torch.utils.data import DataLoader
import random
import numpy as np


class TrainProbingTask(Task):
    def __init__(self, **kwargs):
        self.per_gpu_batch_size = kwargs.get("per_gpu_batch_size", 16)
        self.cuda = kwargs.pop("cuda", True)
        super(TrainProbingTask, self).__init__(**kwargs)

    def set_seed(self, n_gpu, seed=42):
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if n_gpu > 0:
            torch.cuda.manual_seed_all(seed)

    def start_training_process(
        self,
        train_loader,
        test_loader,
        dev_loader,
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
            dev_dataset,
            device,
            n_gpu,
            eval_fn,
        )

        score = self.eval(
            best_model,
            test_data_loader,
            test_dataset,
            device,
            n_gpu,
            eval_fn,
            mode="test",
        )

        return outputs

    @overrides
    def run(self, tasks: Dict, experiments: Dict):
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
        for id_task, content_tasks in tasks.items():
            for id_model, model_content in content_tasks["models"].items():
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
                model_test_data_loader = DataLoader(
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
                control_test_data_loader = DataLoader(
                    model_content["control"]["test"],
                    batch_size=train_batch_size,
                    shuffle=False,
                )

                print(model_content)

    def train(
        self,
        model,
        criterion,
        train_dataloader,
        dev_dataloader,
        dev_dataset,
        device,
        n_gpu,
        eval_fn,
        output_dir,
        save_optimizer,
        eval_params,
    ):
        results = {}
        best_score = 0.0

        optimizer = optim.Adam(model.parameters())

        global_step = 0
        epochs_trained = 0
        steps_trained_in_current_epoch = 0

        tr_loss, logging_loss = 0.0, 0.0
        model.zero_grad()
        train_iterator = trange(
            epochs_trained,
            int(self.num_train_epochs),
            desc="Epoch",
        )

        for epoch in train_iterator:
            epoch_iterator = tqdm(train_dataloader, desc="Iteration")
            epoch_loss = 0
            for step, batch in enumerate(epoch_iterator):
                model.train()
                batch = tuple(t.to(device) for t in batch)

                input_model = {
                    "representation": batch[0],
                    "labels": batch[1],
                }

                output = model(**input_model)

                loss = output["loss"]

                epoch_loss += loss.item()

                if n_gpu > 1:
                    loss = (
                        loss.mean()
                    )  # mean() to average on multi-gpu parallel training
                if self.gradient_accumulation_steps > 1:
                    loss = loss / self.gradient_accumulation_steps

                loss.backward()

                tr_loss += loss.item()
                if (step + 1) % self.gradient_accumulation_steps == 0:
                    torch.nn.utils.clip_grad_norm_(
                        model.parameters(), self.max_grad_norm
                    )

                    optimizer.step()
                    model.zero_grad()
                    global_step += 1

                    if self.logging_steps > 0 and global_step % self.logging_steps == 0:
                        loss_scalar = (tr_loss - logging_loss) / self.logging_steps

                        epoch_iterator.set_description(
                            f"Loss :{loss_scalar} LR: {learning_rate_scalar}"
                        )

                        logging_loss = tr_loss

            score = self.eval(
                criterion,
                model,
                dev_dataloader,
                dev_dataset,
                device,
                n_gpu,
                eval_fn,
                eval_params,
                mode="dev",
            )
            results[epoch] = score

            with torch.no_grad():
                if score > best_score:
                    logger.success(f"Saving new model with best F1-score: {score}")
                    best_model = model
                    best_score = score

        return bert_model

    def eval(
        self,
        criterion,
        model,
        dataloader,
        dataset,
        device,
        n_gpu,
        eval_fn,
        eval_params,
        mode,
    ):
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
                preds = output["preds"]

            nb_eval_steps += 1
            if preds is None:
                preds = preds.detach().cpu().numpy()
                out_label_ids = input_model["labels"].detach().cpu().numpy()

            else:
                preds = np.append(preds, preds.detach().cpu().numpy(), axis=0)

                out_label_ids = np.append(
                    out_label_ids, input_model["labels"].detach().cpu().numpy(), axis=0
                )

        eval_loss = eval_loss / nb_eval_steps

        score = None
        if eval_fn is not None:
            score = eval_fn(preds, out_label_ids)
            logger.info(f"Score:{score}")

        return score, preds
