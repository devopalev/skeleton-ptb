import logging
from typing import Any

from telegram.ext import CallbackContext, ExtBot

from apps.common.repositories.repository import AbstractRepository, Repository


logger = logging.getLogger(__name__)


class CustomContext(CallbackContext[ExtBot[None], dict[Any, Any], dict[Any, Any], dict[Any, Any]]):
    """Custom class for context."""

    db_storage: AbstractRepository = Repository()
