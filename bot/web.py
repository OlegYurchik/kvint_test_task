import json
import logging
from urllib.parse import urljoin

from aiohttp import web
from botovod.agents.telegram.types import TelegramKeyboard

from dialogs import Dialog


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


async def handler(agent, chat, message, follower, **scope):
    follower_state = await scope["db_client"].get_follower_state(follower_id=follower.id)
    if follower_state is None:
        follower_state = await scope["db_client"].create_follower_state(follower=follower)
    data = json.loads(follower_state.data)

    dialog = Dialog(state=follower_state.state)
    dialog.handle(text=message.text, data=data)

    await scope["db_client"].update_follower_state(
        follower_state=follower_state,
        state=dialog.state,
        data=dialog.data,
    )
    keyboard = None
    if dialog.ANSWERS[dialog.state]:
        keyboard = TelegramKeyboard(
            buttons=([answer] for answer in dialog.ANSWERS[dialog.state]),
            resize=True,
            one_time=True,
        )
    await agent.a_send_message(chat=chat, text=dialog.answer, keyboard=keyboard)
