import asyncio
import logging
from typing import Any, Optional

from telegram import Update
from telegram.ext import Application, ContextTypes, ExtBot, JobQueue, CallbackContext

import settings
from apps.telegram_bot import setup
from apps.telegram_bot.core.context import CustomContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def create_telegram_app() -> (
    Application[
        ExtBot[None],
        CustomContext,
        dict[Any, Any],
        dict[Any, Any],
        dict[Any, Any],
        JobQueue[CallbackContext[ExtBot[None], dict[Any, Any], dict[Any, Any], dict[Any, Any]]],
    ]
):
    """Start the bot."""
    if not settings.BOT_TOKEN:
        raise ValueError('BOT_TOKEN must be set')

    context_types = ContextTypes(context=CustomContext)
    app = Application.builder().token(settings.BOT_TOKEN).context_types(context_types).build()

    await setup(app)
    return app


async def run_telegram_app(
    app: Optional[
        Application[
            ExtBot[None],
            CustomContext,
            dict[Any, Any],
            dict[Any, Any],
            dict[Any, Any],
            JobQueue[CallbackContext[ExtBot[None], dict[Any, Any], dict[Any, Any], dict[Any, Any]]],
        ]
    ] = None,
) -> None:
    app = app or await create_telegram_app()

    if not app.updater:
        raise ValueError('Updater must be set')

    async with app:  # Calls `initialize` and `shutdown`
        await app.start()
        await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        await asyncio.Future()  # endless waiting


async def run_telegram_app_daemon() -> (
    Application[
        ExtBot[None],
        CustomContext,
        dict[Any, Any],
        dict[Any, Any],
        dict[Any, Any],
        JobQueue[CallbackContext[ExtBot[None], dict[Any, Any], dict[Any, Any], dict[Any, Any]]],
    ]
):
    app = await create_telegram_app()
    asyncio.create_task(run_telegram_app(app=app))
    return app


if __name__ == '__main__':
    asyncio.run(run_telegram_app())
