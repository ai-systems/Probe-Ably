from pathlib import Path

CONFIG_FOLDER = Path(__file__).parent
SCHEMA_TEMPLATE_FILE = CONFIG_FOLDER.joinpath('input_json_schema.json')
DEFAULT_PROBING_SETUP = CONFIG_FOLDER.joinpath('default_probing_setup.json')