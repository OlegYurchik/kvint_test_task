import os

from .common import Settings


current_settings = Settings()

SERVICE_NAME = "kvinttest.bot"
LOGGING_LEVEL = os.environ.get("KVINTTEST_LOGGING_LEVEL", "INFO")
