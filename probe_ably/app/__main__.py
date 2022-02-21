from probe_ably.metrics import ProcessMetricTask
from probe_ably.utils import ReadInputTask
from probe_ably.probing import TrainProbingTask
from probe_ably import ProbingExperiment
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
process_metric_task = ProcessMetricTask()


class ProbingThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.results = None
        self.task_loop_bar = None
        self.reps_loop_bar = None
        self.probes_loop_bar = None
        self.results = None

    async def set_config(self, config_file):
        self.parsed_input = await read_input_task.run(config_file)

    def run(self):
        experiment = ProbingExperiment.from_parsed_input(self.parsed_input, thread=self)
        results = experiment.run()
        return results

        # try:
        #     prepared_data = prepare_data_probing.run(
        #         self.config["tasks"], self.config["probing_setup"]
        #     )
        #     train_results = probing_task.run(prepared_data, 
        #             self.config["probing_setup"],
        #             thread=self)
        #     processed_results = process_metric_task.run(train_results, 
        #             self.config["probing_setup"]
        #     )
        # except TypeError:
        #     raise ValueError("Has the config been set?")

app = FastAPI()
app.probing_thread = ProbingThread()

@app.post("/start_probing")
async def start_probing(background_tasks: BackgroundTasks, config_file: UploadFile = File(...), ):
    await app.probing_thread.set_config(config_file)
    results = await run_in_threadpool(app.probing_thread.run)
    print(results)
    app.probing_thread.results = results
    return results

@app.get('/model_progress')
def model_progress():
    prog = app.probing_thread.reps_loop_bar.format_dict
    return prog

@app.get('/task_progress')
async def task_progress():
    prog = app.probing_thread.task_loop_bar.format_dict
    return prog
    
@app.get('/probes_progress')
def probes_progress():
    prog = app.probing_thread.probes_loop_bar.format_dict
    return prog

@app.get('/results')
def get_results():
    results = app.probing_thread.results
    return results


app.mount("/", StaticFiles(directory=build_dir, html = True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)