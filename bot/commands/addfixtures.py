import asyncio
import logging

from database.client import DBClient
from .command import Command


logger = logging.getLogger(__name__)


class AddFixturesCommand(Command):
    def process(self):
        self.session["db_client"] = DBClient(
            engine=self.settings.database.engine,
            host=self.settings.database.host,
            port=self.settings.database.port,
            name=self.settings.database.name,
            username=self.settings.database.user,
            password=self.settings.database.password,
        )

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.a_run())

    async def a_run(self):
        await self.session["db_client"].connect()
        await self.session["db_client"].add_fixtures()
