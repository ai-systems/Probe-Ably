import json
from typing import Dict

from loguru import logger
from overrides import overrides
from prefect import Task
from probe_ably.service.server.web_server import WebServer


class VisualiaztionTask(Task):
    def run(self, processed_data: Dict):
        logger.info("Launching server for visualization")
        web_server = WebServer(processed_data)
        # with open(f"{web_server.get_path()}/data.json", "w") as f:
        # json.dump(processed_data, f)
        web_server.start()
