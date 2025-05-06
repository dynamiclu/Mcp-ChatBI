import os
import socket
import toml
import shutil
from common.log import logger

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
config_file = f"{root_dir}/config/config.toml"

OPEN_CROSS_DOMAIN = True

def load_config():
    if os.path.isdir(config_file):
        shutil.rmtree(config_file)

    if not os.path.isfile(config_file):
        example_file = f"{root_dir}/config.example.toml"
        if os.path.isfile(example_file):
            shutil.copyfile(example_file, config_file)
            logger.info(f"copy config.example.toml to config.toml")

    logger.info(f"load config from file: {config_file}")

    try:
        _config_ = toml.load(config_file)
    except Exception as e:
        logger.warning(f"load config failed: {str(e)}, try to load as utf-8-sig")
        with open(config_file, mode="r", encoding="utf-8-sig") as fp:
            _cfg_content = fp.read()
            _config_ = toml.loads(_cfg_content)
    return _config_



_cfg = load_config()
app = _cfg.get("model", {})
server = _cfg.get("server", {})

if server:
    API_HOST = server.get("API_HOST", "127.0.0.1")
    API_PORT = server.get("API_PORT", 8899)
    API_URL = f"http://{API_HOST}:{API_PORT}"
    WEB_SERVER_HOST = server.get("WEB_SERVER_HOST", "127.0.0.1")
    WEB_SERVER_PORT = server.get("WEB_SERVER_PORT", 8080)
else:
    API_HOST = "127.0.0.1"
    API_PORT = 8899
    API_URL = f"http://{API_HOST}:{API_PORT}"
    WEB_SERVER_HOST = "127.0.0.1"
    WEB_SERVER_PORT = 8080
