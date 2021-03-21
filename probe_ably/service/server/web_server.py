import os
from pathlib import Path

from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS, cross_origin

this_filepath = Path(os.path.abspath(__file__))
this_dirpath = this_filepath.parent.parent


class WebServer:
    def __init__(self):
        self.app = Flask(
            __name__,
            static_folder=str(this_dirpath.joinpath("build")),
            static_url_path="",
        )
        self.cors = CORS(self.app)
        self.app.config["CORS_HEADERS"] = "Content-Type"

        self.app.add_url_rule("/", view_func=self.serve)
        self.app.add_url_rule("/sample", view_func=self.serve_data)

    def serve(self):
        print(this_dirpath)
        return send_from_directory(self.app.static_folder, "index.html")

    def serve_data(self):
        return jsonify(
            {
                "aux_tasks": [
                    {
                        "id": "1",
                        "name": "Task name 1",
                        "probings": [
                            {
                                "model_name": "MLP",
                                "probing_results": [
                                    {
                                        "x_axis": "Number of Parameter",
                                        "y_axis": "Accuracy",
                                        "chart_data": [
                                            {
                                                "id": "japan",
                                                "color": "hsl(190, 70%, 50%)",
                                                "data": [
                                                    {
                                                        "x": "plane",
                                                        "y": 175,
                                                    },
                                                    {
                                                        "x": "helicopter",
                                                        "y": 295,
                                                    },
                                                    {
                                                        "x": "boat",
                                                        "y": 54,
                                                    },
                                                ],
                                            },
                                        ],
                                    },
                                    {
                                        "x_axis": "Number of Parameter",
                                        "y_axis": "Selectivity",
                                        "chart_data": [
                                            {
                                                "id": "japan",
                                                "color": "hsl(190, 70%, 50%)",
                                                "data": [
                                                    {
                                                        "x": "plane",
                                                        "y": 175,
                                                    },
                                                    {
                                                        "x": "helicopter",
                                                        "y": 295,
                                                    },
                                                    {
                                                        "x": "boat",
                                                        "y": 54,
                                                    },
                                                    {
                                                        "x": "train",
                                                        "y": 126,
                                                    },
                                                ],
                                            },
                                        ],
                                    },
                                ],
                            },
                            {
                                "model_name": "Linear",
                                "probing_types": [{"index": 0, "name": "Accuracy"}],
                                "probing_results": [
                                    {
                                        "x_axis": "Number of Parameter",
                                        "y_axis": "Accuracy",
                                        "chart_data": [
                                            {
                                                "id": "japan",
                                                "color": "hsl(190, 70%, 50%)",
                                                "data": [
                                                    {
                                                        "x": "plane",
                                                        "y": 175,
                                                    },
                                                    {
                                                        "x": "helicopter",
                                                        "y": 295,
                                                    },
                                                ],
                                            },
                                        ],
                                    },
                                ],
                            },
                        ],
                    },
                ],
            }
        )

    def start(self, port: int = 8031):
        self.app.run(port=port, host="0.0.0.0")


server = WebServer()
server.start()
