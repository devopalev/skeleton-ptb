from telegram import InlineKeyboardMarkup

from apps.telegram_bot.tg.elements.buttons import IgnoreButton


class Exemple(InlineKeyboardMarkup):
    def __init__(self) -> None:
        keyboard = [[IgnoreButton('Example')]]
        super().__init__(keyboard)
