import logging
from urllib.parse import urljoin

from aiohttp import web


logger = logging.getLogger(__name__)


def generate_telegram_bot_route():
    return "telegram"


def generate_telegram_bot_url(settings):
    return urljoin(
        settings.bot.webhook_url,
        generate_telegram_bot_route(),
    )


async def telegram_view(request):
    status, headers, body = await request.app["botovod"].a_listen(
        name="telegram",
        headers=request.headers,
        body=await request.text(),
    )
    return web.Response(status=status, headers=headers, body=body)
