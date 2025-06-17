from functools import partial

from telegram.helpers import escape_markdown

from apps.telegram_bot.tg.elements.base import BaseMessage


escape_markdown_2 = partial(escape_markdown, version=2)


class HelpMessage(BaseMessage):
    text = 'Что начать введите / и следуйте подсказкам'


class BadCallbackMessage(BaseMessage):
    text = 'Не удалось распознать кнопку, возможно она устарела'


class StartMessage(BaseMessage):
    def __init__(self, fullname: str) -> None:
        self.text = f'Привет, {fullname}!\nИспользуй /help для вызова справки'
