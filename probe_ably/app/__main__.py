from probe_ably.metrics import ProcessMetricTask
from probe_ably.utils import ReadInputTask
from probe_ably.probing import TrainProbingTask, PrepareDataForProbingTask

from pathlib import Path
import threading
import os

from fastapi import FastAPI, UploadFile, File, Request, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.concurrency import run_in_threadpool
import uvicorn

from pydantic import BaseModel


app_dir = Path(os.path.abspath(__file__)).parent
build_dir = app_dir.joinpath('build')
print(build_dir)

# INPUT_FILE = "./tests/sample_files/test_input/multi_task_multi_model_with_control.json"
probing_task = TrainProbingTask()
read_input_task = ReadInputTask()
prepare_data_probing = PrepareDataForProbingTask()
process_metric_task = ProcessMetricTask()


class ProbingThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.results = None
        self.task_loop_bar = None
        self.model_loop_bar = None
        self.probes_loop_bar = None
        self.config = None

    async def set_config(self, config_file):
        self.config = await read_input_task.run(config_file)

    def run(self):
        try:
            prepared_data = prepare_data_probing.run(
                self.config["tasks"], self.config["probing_setup"]
            )
            train_results = probing_task.run(prepared_data, 
                    self.config["probing_setup"],
                    thread=self)
            processed_results = process_metric_task.run(train_results, 
                    self.config["probing_setup"]
            )
        except TypeError:
            raise ValueError("Has the config been set?")

        return processed_results

app = FastAPI()
app.probing_thread = ProbingThread()

@app.post("/start_probing")
async def start_probing(background_tasks: BackgroundTasks, config_file: UploadFile = File(...), ):
    await app.probing_thread.set_config(config_file)
    results = await run_in_threadpool(app.probing_thread.run)
    return results

@app.get('/model_progress')
def model_progress():
    prog = app.probing_thread.model_loop_bar.format_dict
    return prog

@app.get('/task_progress')
async def task_progress():
    prog = app.probing_thread.task_loop_bar.format_dict
    return prog
    
@app.get('/probes_progress')
def probes_progress():
    prog = app.probing_thread.probes_loop_bar.format_dict
    return prog


app.mount("/", StaticFiles(directory=build_dir, html = True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)