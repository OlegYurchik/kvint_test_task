import argparse
from functools import wraps
import json
import logging
import logging.config
import os
import yaml


logger = logging.getLogger(__name__)


def chdir(path):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            current_path = os.getcwd()
            os.chdir(path)
            logger.debug("Change directory from '%s' to '%s'", current_path, path)
            result = function(*args, **kwargs)
            os.chdir(current_path)
            logger.debug("Change directory from '%s' to '%s'", path, current_path)
            return result
        return wrapper
    return decorator


def generate_dsn(engine, host=None, port=None, name=None, username=None, password=None, **params):
    dsn = f"{engine}://"
    if username and password:
        dsn += f"{username}:{password}@"
    elif username:
        dsn += f"{username}@"
    dsn += host
    if port:
        dsn += f":{port}"
    if name:
        dsn += f"/{name}"
    if params:
        params = "&".join(f"{key}={value}" for key, value in params.items())
        dsn += f"?{params}"

    return dsn


def parse_args(message, commands):
    parser = argparse.ArgumentParser(message)
    parser.add_argument(
        "command",
        type=str,
        choices=commands,
        help="Command",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="Path to .ini file with configuration",
    )

    return parser.parse_args()


def set_logging_config(level, filetype, filename):
    if filetype == "ini":
        logging.config.fileConfig(filename)
    elif filetype == "yaml":
        with open(filename, "rt") as yaml_file:
            logging.config.dictConfig(yaml.safe_load(yaml_file))
    logging.getLogger().setLevel(level)
