import datetime
import logging
import os

import alembic.config

from utils import chdir
from .command import Command


logger = logging.getLogger(__name__)


class MakeMigrationsCommand(Command):
    ALEMBIC_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    @chdir(ALEMBIC_PATH)
    def process(self):
        alembic.config.main(argv=(
            "revision",
            "--autogenerate",
            "-m",
            datetime.datetime.now().strftime("%Y%m%dt%H%M%S"),
        ))
        logger.info("Make migrations")
        alembic.config.main(argv=("upgrade", "head"))
        logger.info("Migrate")
