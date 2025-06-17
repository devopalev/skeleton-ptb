from apps.telegram_bot.tg.elements.base import BaseButton
from apps.telegram_bot.tg.elements.utils import CallbackBuilder


class IgnoreButton(BaseButton):
    BASE_CALLBACK = CallbackBuilder('ignore')

    def __init__(self, text: str) -> None:
        super().__init__(text=text, callback_data='menu:close')


class CloseMenuButton(BaseButton):
    BASE_CALLBACK = CallbackBuilder('menu', 'close')

    def __init__(self) -> None:
        super().__init__(text='✖️ Закрыть меню', callback_data=str(self.BASE_CALLBACK))


class RobotCancelButton(BaseButton):
    BASE_CALLBACK = CallbackBuilder('cancel')

    def __init__(self) -> None:
        super().__init__(text='✖️ Отменить', callback_data=str(self.BASE_CALLBACK))
