import asyncio
import logging
import ssl

from aiohttp import web
from botovod import Botovod
from botovod.agents.telegram import TelegramAgent

from database.client import DBClient
from web import generate_telegram_bot_route, generate_telegram_bot_url, handler, telegram_view
from .command import Command


logger = logging.getLogger(__name__)


class RunCommand(Command):
    def process(self):
        if (self.settings.bot is None or
                self.settings.bot.webhook_url is None or
                self.settings.bot.port is None):
            self.session["app"] = None
        else:
            self.session["app"] = web.Application()
        self.session["db_client"] = DBClient(
            engine=self.settings.database.engine,
            host=self.settings.database.host,
            port=self.settings.database.port,
            name=self.settings.database.name,
            username=self.settings.database.user,
            password=self.settings.database.password,
        )
        self.session["botovod"] = Botovod(dbdriver=self.session["db_client"])
        self.session["botovod"]["db_client"] = self.session["db_client"]

        self.session["loop"] = asyncio.get_event_loop()
        self.session["loop"].run_until_complete(self.init())

        try:
            self.session["loop"].run_forever()
        finally:
            asyncio.get_event_loop().run_until_complete(self.close())

    async def init(self):
        await self.session["db_client"].connect()

        self.session["botovod"].clear_handlers()
        self.session["botovod"].add_handler(handler)

        await self.init_telegram()

        if self.session["app"] is None:
            return

        self.session["app"]["botovod"] = self.session["botovod"]
        self.session["app"]["db_client"] = self.session["db_client"]
        ssl_context = None

        if (self.settings.bot.certificate_path is not None
                and self.settings.bot.privatekey_path is not None):
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.load_cert_chain(
                self.settings.bot.certificate_path,
                self.settings.bot.privatekey_path,
            )
        self.session["loop"].create_task(web._run_app(
            app=self.session["app"],
            port=self.settings.bot.port,
            ssl_context=ssl_context,
        ))

    async def init_telegram(self):
        webhook_url = None
        certificate_path = None
        method = TelegramAgent.POLLING
        if (self.settings.bot is not None
                and self.settings.bot.webhook_url is not None
                and self.settings.bot.port is not None):
            webhook_url = generate_telegram_bot_url(settings=self.settings)
            method = TelegramAgent.WEBHOOK
            certificate_path = self.settings.bot.certificate_path

        agent = TelegramAgent(
            token=self.settings.bot.telegram_token,
            method=method,
            webhook_url=webhook_url,
            certificate_path=certificate_path,
        )
        self.session["botovod"].add_agent("telegram", agent)
        if self.session["app"] is not None:
            self.session["app"].router.add_route(
                method="*",
                path=f"/{generate_telegram_bot_route()}",
                handler=telegram_view,
            )
        await agent.a_start()

    async def close(self):
        await self.session["botovod"].a_stop()
        await self.session["db_client"].close()
