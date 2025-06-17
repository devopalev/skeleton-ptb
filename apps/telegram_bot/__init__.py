from typing import Any

from telegram.ext import Application, ExtBot, JobQueue, CallbackContext

from apps.telegram_bot.core.context import CustomContext
from apps.telegram_bot.tg.handlers.common import error_handler, common_router


async def setup(
    app: Application[
        ExtBot[None],
        CustomContext,
        dict[Any, Any],
        dict[Any, Any],
        dict[Any, Any],
        JobQueue[CallbackContext[ExtBot[None], dict[Any, Any], dict[Any, Any], dict[Any, Any]]],
    ],
) -> None:
    app.add_handlers(common_router.get_handlers())
    app.add_error_handler(error_handler)  # type: ignore[arg-type]

    commands = common_router.get_bot_commands()
    await app.bot.set_my_commands(commands)
