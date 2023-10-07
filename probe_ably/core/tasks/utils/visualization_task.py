import json
import webbrowser
from typing import Dict

from loguru import logger
from prefect import Task
from probe_ably.service.server.web_server import WebServer


class VisualiaztionTask(Task):
    def run(self, processed_data: Dict):
        logger.info("Launching server for visualization")
        web_server = WebServer(processed_data)
        # with open(f"{web_server.get_path()}/data.json", "w") as f:
        # json.dump(processed_data, f)
        web_server.start()

        ip_address = "http://127.0.0.1:8031/"

        try:
            webbrowser.get("google-chrome").open(ip_address)
        except:
            logger.info(
                f"Tried to launch Google Chrom and Failed. Visit: {ip_address} to view the visualization"
            )
