import logging.config

from pythonjsonlogger import jsonlogger

import settings


class JsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        kwargs['json_ensure_ascii'] = kwargs.get('json_ensure_ascii', False)
        super().__init__(*args, **kwargs)


LOG_SETTINGS = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'text': {
            'format': '%(asctime)s [%(levelname)s] %(name)s | %(message)s',
        },
        'json': {
            '()': JsonFormatter,
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'text',
        },
        'json': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
    },
    'loggers': {
        '': {
            'level': settings.LOG_LEVEL or logging.INFO,
            'handlers': [settings.LOG_HANDLER or 'console'],
        }
    },
}


def setup_logs() -> None:
    logging.config.dictConfig(LOG_SETTINGS)
