import logging
import os
import platform

from environs import Env


env = Env()
env.read_env()

##############################################
# Systems
##############################################

DEBUG = env.bool('DEBUG', default=False)
RELEASE = env.str('RELEASE', default=None)
HOSTNAME = env.str('HOSTNAME', default=platform.node())
ENVIRONMENT = env.str('ENVIRONMENT', default='local')

LOG_LEVEL = env.str(
    name='LOG_LEVEL',
    default=logging.getLevelName(logging.DEBUG if DEBUG else logging.INFO),
)
LOG_HANDLER = env.str(name='LOG_HANDLER', default='console')
SANDBOX = env.bool('SANDBOX', default=False)

##############################################
# Database
##############################################

POSTGRES_USER = env.str('POSTGRES_USER', default=None)
POSTGRES_PASSWORD = env.str('POSTGRES_PASSWORD', default=None)
POSTGRES_DB = env.str('POSTGRES_DB', default=None)
POSTGRES_HOST = env.str('POSTGRES_HOST', default=None)
POSTGRES_PORT = env.str('POSTGRES_PORT', default=None)

POSTGRES_DSN = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

POSTGRES_MIN_POOL_SIZE = env.int('POSTGRES_MIN_POOL_SIZE', default=2)
POSTGRES_MAX_POOL_SIZE = env.int('POSTGRES_MAX_POOL_SIZE', default=10)

APP_MIGRATIONS_PATH = os.path.abspath('migrations')


##############################################
# Tokens
##############################################

BOT_TOKEN = env.str('BOT_TOKEN', default=None)
