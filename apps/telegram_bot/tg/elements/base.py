import typing

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode

from apps.telegram_bot.tg.elements.utils import CallbackBuilder


class BaseMessage:
    """
    Интерфейс сообщения. Служит для сборки текста и клавиатур.
    """

    text: str
    parse_mode: typing.Optional[ParseMode] = None
    reply_markup: typing.Optional[InlineKeyboardMarkup] = None


class BaseButton(InlineKeyboardButton):
    BASE_CALLBACK: CallbackBuilder
