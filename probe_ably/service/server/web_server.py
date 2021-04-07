import os
from pathlib import Path

from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS, cross_origin

this_filepath = Path(os.path.abspath(__file__))
this_dirpath = this_filepath.parent.parent
import json

class WebServer:
    def __init__(self, processed_data):
        self.app = Flask(
            __name__,
            static_folder=str(this_dirpath.joinpath("build")),
            static_url_path="",
        )
        self.cors = CORS(self.app)
        self.app.config["CORS_HEADERS"] = "Content-Type"
        self.processed_data = processed_data

        self.app.add_url_rule("/", view_func=self.serve)
        self.app.add_url_rule("/sample", view_func=self.serve_data)

    def get_path(self):
        return this_dirpath

    def serve(self):
        print(this_dirpath)
        return send_from_directory(self.app.static_folder, "index.html")

    def serve_data(self):
        # with open(f"{self.get_path()}/data.json", "r") as f:
            # data = json.load(f)
        return jsonify({"aux_tasks": self.processed_data})

    def start(self, port: int = 8031):
        self.app.run(port=port, host="0.0.0.0")
