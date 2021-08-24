from probe_ably.core.tasks.probing import TrainProbingTask
from probe_ably.core.tasks.metric_task import ProcessMetricTask
from probe_ably.core.tasks.probing import PrepareDataForProbingTask, TrainProbingTask
from probe_ably.core.tasks.utils import ReadInputTask, VisualiaztionTask

from pathlib import Path
import threading
import os

from fastapi import FastAPI, UploadFile, File, Request, BackgroundTasks
from fastapi.staticfiles import StaticFiles
import uvicorn

app_dir = Path(os.path.abspath(__file__)).parent
build_dir = app_dir.joinpath('build')
print(build_dir)

INPUT_FILE = "./tests/sample_files/test_input/multi_task_multi_model_with_control.json"
probing_task = TrainProbingTask()
read_input_task = ReadInputTask()
prepare_data_probing = PrepareDataForProbingTask()
process_metric_task = ProcessMetricTask()
visualization_task = VisualiaztionTask()

app = FastAPI()

@app.get("/user_config")
def user_config():
    return {'thing': 'other'}

@app.post("/start_probing")
async def start_probing(config_file: UploadFile = File(...)):
    results = await probing_flow(config_file)
    return {"status": "probing!"}

async def probing_flow(config):
    parsed_input = await read_input_task.run(config)
    prepared_data = prepare_data_probing.run(
        parsed_input["tasks"], parsed_input["probing_setup"]
    )
    train_results = probing_task.run(prepared_data, 
            parsed_input["probing_setup"])
    processed_results = process_metric_task.run(train_results, 
            parsed_input["probing_setup"]
    )
    return processed_results


class ProbingThread(threading.Thread):
    def __init__(self):
        super().__init__()
    
# class ProbingThread(threading.Thread):
#     def __init__(self):
#         super().__init__()
#         self.results = None
#         self.task_loop_bar = None
#         self.model_loop_bar = None
#         self.probes_loop_bar = None

#     def run(self,config_file=INPUT_FILE):
#         # probing flow
#         parsed_input = read_input_task.run(config_file)
#         prepared_data = prepare_data_probing.run(
#             parsed_input["tasks"], parsed_input["probing_setup"]
#         )
#         train_results = probing_task.run(prepared_data, 
#                 parsed_input["probing_setup"], 
#                 thread=self)
#         processed_results = process_metric_task.run(train_results, 
#                 parsed_input["probing_setup"]
#         )
#         self.finished = 1
#         self.results = processed_results

# threads = {}

# @app.route('/')
# def serve():
#     print(static_folder)
#     return send_from_directory(app.static_folder, 'index.html')

# @app.route('/time')
# def get_current_time():
#     return {'time': time.time()}


# @app.route('/process')
# def process():
#     global threads

#     thread_id = 1
#     threads[thread_id] = ProbingThread()
#     threads[thread_id].start()
#     return 'task id: #%s' % thread_id

# @app.route('/model_progress')
# def model_progress(thread_id=1):
#     global threads

#     return jsonify(threads[thread_id].model_loop_bar.format_dict)

# @app.route('/task_progress')
# def task_progress(thread_id=1):
#     global threads

#     return jsonify(threads[thread_id].task_loop_bar.format_dict)

# @app.route('/probes_progress')
# def probes_progress(thread_id=1):
#     global threads

#     return jsonify(threads[thread_id].probes_loop_bar.format_dict)


# @app.route('/results')
# def results(thread_id=1):
#     global threads

#     return jsonify({"aux_tasks": threads[thread_id].results})

# app.run(port=8031, host="0.0.0.0")

app.mount("/", StaticFiles(directory=build_dir, html = True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)