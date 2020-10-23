import configparser
import json
import logging
import os
from random import choice
from string import ascii_lowercase, digits

from jsonschema import validate
import yaml


logger = logging.getLogger(__name__)


class Section:
    SCHEMAS_DIR = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "schemas",
    )

    def __init__(self, data, **info):
        self._options = {}
        data = self.add_additional_info(data, **info)
        data = self.add_default_values(data)
        with open(os.path.join(self.SCHEMAS_DIR, self.SCHEMA_FILENAME), "rt") as file:
            schema = yaml.unsafe_load(file)
        logger.info("Load %s settings validation schema", self.SCHEMA_FILENAME)
        validate(instance=data, schema=schema)
        logger.debug("Section validated with %s settings validation schema", self.SCHEMA_FILENAME)

        for key, value in data.items():
            self._options[key] = value

    def __getattr__(self, item):
        return self._options.get(item)

    @staticmethod
    def default_values():
        return {}

    @classmethod
    def add_default_values(cls, data):
        new_data = data.copy()
        for name, value in cls.default_values().items():
            if name not in new_data:
                new_data[name] = value
        return new_data

    @staticmethod
    def add_additional_info(data, **info):
        new_data = data.copy()
        new_data.update(info)
        return new_data


class InstanceSection(Section):
    SCHEMA_FILENAME = "instance.yaml"

    @staticmethod
    def default_values():
        return {"id": "".join(choice(ascii_lowercase + digits) for _ in range(64))}


class LoggingSection(Section):
    SCHEMA_FILENAME = "logging.yaml"

    @staticmethod
    def default_values():
        return {"level": "INFO"}


class DatabaseSection(Section):
    SCHEMA_FILENAME = "database.yaml"


class BotSection(Section):
    SCHEMA_FILENAME = "bot.yaml"


class Settings:
    SECTIONS = ("instance", "logging", "database", "bot")

    def __init__(self):
        self.instance = None
        self.logging = None
        self.database = None
        self.bot = None

    @classmethod
    def transform(cls, value):
        try:
            value = json.loads(value)
        except Exception:
            pass
        return value

    def fill(self, data, service):
        self.instance = InstanceSection(data.get("instance", {}), service=service)
        self.logging = LoggingSection(data.get("logging", {}))
        self.database = DatabaseSection(data["database"]) if "database" in data else None
        self.bot = BotSection(data["bot"]) if "bot" in data else None

    def from_env(self, service):
        data = {}
        for variable, value in os.environ.items():
            try:
                app_name, section, option = map(str.lower, variable.split("_", 2))
            except ValueError:
                continue
            if (app_name != "kvinttest" or
                    section not in self.SECTIONS or
                    not option or (not option[0].isalpha() and not option[0] == "_")):
                continue

            if section not in data:
                data[section] = {}
            data[section][option] = self.transform(value)

        self.fill(data, service=service)

    def from_ini(self, filename, service):
        if not os.path.isfile(filename):
            logger.error("Cannot load '%s': not exists or not a file", filename)

        config = configparser.ConfigParser()
        config.read(filename)

        data = {}
        for name, section in config.items():
            name = name.lower()
            data[name] = {}
            for option, value in section.items():
                option = option.lower()
                data[name][option] = self.transform(value)

        self.fill(data, service=service)
