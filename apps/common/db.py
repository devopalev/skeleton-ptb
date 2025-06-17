import asyncpg
import ujson
from asyncpg import Connection, Pool


from yoyo import read_migrations
from yoyo import get_backend

import settings


DEFAULT_POOL = 'default'
_POOL_REGISTRY: dict[str, Pool] = {}


async def setup_db() -> None:
    async def _on_init_connection(conn: asyncpg.Connection) -> None:
        await conn.set_type_codec(
            'jsonb',
            encoder=ujson.dumps,
            decoder=ujson.loads,
            schema='pg_catalog',
        )

    _POOL_REGISTRY[DEFAULT_POOL] = await asyncpg.create_pool(
        dsn=settings.POSTGRES_DSN,
        init=_on_init_connection,
        min_size=settings.POSTGRES_MIN_POOL_SIZE,
        max_size=settings.POSTGRES_MAX_POOL_SIZE,
        connection_class=Connection,
        statement_cache_size=0,
    )


async def connection() -> Pool:
    return _POOL_REGISTRY[DEFAULT_POOL]


def apply_migrations() -> None:
    """
    Инициализация БД, запуск миграций
    """
    backend = get_backend(settings.POSTGRES_DSN)
    migrations = read_migrations(settings.APP_MIGRATIONS_PATH)

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
