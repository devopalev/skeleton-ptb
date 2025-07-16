import asyncio

import typer

import settings
from apps.common.db import apply_migrations, setup_db, shutdown_db
from apps.telegram_bot.app import run_telegram_app, create_telegram_app
from apps.common.logs import setup_logs

app = typer.Typer()


async def core() -> None:
    setup_logs()

    if settings.POSTGRES_HOST:
        apply_migrations()
        await setup_db()

    tg_app = await create_telegram_app()
    await run_telegram_app(app=tg_app)

    await shutdown_db()


@app.command()
def run() -> None:
    asyncio.run(core())


if __name__ == '__main__':
    app()
