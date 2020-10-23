import os

import jsonschema
import pytest
import yaml

from bot.settings import Settings


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "settings")


def get_env():
    env_data_dir = os.path.join(TEST_DATA_DIR, "env")
    for filename in os.listdir(env_data_dir):
        with open(os.path.join(env_data_dir, filename), "rt") as file:
            data = yaml.unsafe_load(file)
        yield (
            data["service"],
            data["env"],
            data["message"],
        )


def get_ini():
    ini_data_dir = os.path.join(TEST_DATA_DIR, "ini")
    for filename in os.listdir(ini_data_dir):
        if not filename.endswith(".yaml"):
            continue
        with open(os.path.join(ini_data_dir, filename), "rt") as file:
            data = yaml.unsafe_load(file)
        yield (
            data["service"],
            os.path.join(ini_data_dir, data["filename"]),
            data["message"],
        )


def get_fill():
    fill_data_dir = os.path.join(TEST_DATA_DIR, "fill")
    for filename in os.listdir(fill_data_dir):
        with open(os.path.join(fill_data_dir, filename), "rt") as file:
            data = yaml.unsafe_load(file)
        yield (
            data["service"],
            data["data"],
            data["message"],
        )


@pytest.mark.parametrize("service, data, message", get_fill())
def test_fill(service, data, message):
    settings = Settings()

    try:
        settings.fill(data=data, service=service)
    except jsonschema.exceptions.ValidationError as exception:
        assert exception.args[0] == message
    else:
        assert message is None


@pytest.mark.parametrize("service, env_variables, message", get_env())
def test_env(service, env_variables, message):
    settings = Settings()

    old_values = {}
    for name, value in env_variables.items():
        if name in os.environ:
            old_values[name] = os.environ[name]
        os.environ[name] = str(value)

    try:
        settings.from_env(service=service)
    except jsonschema.exceptions.ValidationError as exception:
        assert exception.args[0] == message
    else:
        assert message is None
    finally:
        for name in env_variables:
            del os.environ[name]
        for name, value in old_values.items():
            os.environ[name] = value


@pytest.mark.parametrize("service, filename, message", get_ini())
def test_ini(service, filename, message):
    settings = Settings()

    try:
        settings.from_ini(filename=filename, service=service)
    except jsonschema.exceptions.ValidationError as exception:
        assert exception.args[0] == message
    else:
        assert message is None
