import typing

from telegram import InlineKeyboardMarkup
from telegram.constants import ParseMode


class BaseMessage:
    """
    Интерфейс сообщения. Служит для сборки текста и клавиатур.
    """

    text: str
    parse_mode: typing.Optional[ParseMode] = None
    reply_markup: typing.Optional[InlineKeyboardMarkup] = None
