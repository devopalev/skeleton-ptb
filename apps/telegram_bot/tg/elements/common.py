from functools import partial

from telegram.helpers import escape_markdown

from apps.telegram_bot.tg.elements.base import BaseMessage
from apps.telegram_bot.tg.elements.utils import CallbackManager

escape_markdown_2 = partial(escape_markdown, version=2)

IGNORE = CallbackManager('f024dddf-0ad0-49b3-815f-764a7a27b6df')
MENU_CLOSE = CallbackManager('843afce5-a6a6-4e30-987c-f0eede201437')
MENU_CANCEL = CallbackManager('a4efad22-1e6a-48c4-ab4b-10f0a308b1a7')


class HelpMessage(BaseMessage):
    text = 'Что начать введите / и следуйте подсказкам'


class BadCallbackMessage(BaseMessage):
    text = 'Не удалось распознать кнопку, возможно она устарела'


class StartMessage(BaseMessage):
    def __init__(self, fullname: str) -> None:
        self.text = f'Привет, {fullname}!\nИспользуй /help для вызова справки'
