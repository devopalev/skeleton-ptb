import typing

from telegram import BotCommand
from telegram._utils.types import JSONDict
from telegram.ext import CommandHandler

from apps.telegram_bot import CustomContext


class CommandHandlerCustom(CommandHandler[CustomContext]):
    def __init__(
        self,
        command: str,
        *args: typing.Any,
        description: typing.Optional[str] = None,
        api_kwargs: typing.Optional[JSONDict] = None,
        show_command: bool = True,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__(command, *args, **kwargs)
        self._custom_command = command
        self._custom_description = description
        self.show_command = show_command
        self._api_kwargs = api_kwargs

    def build_bot_command(self) -> BotCommand:
        return BotCommand(
            command=self._custom_command,
            description=self._custom_description or self._custom_command,
            api_kwargs=self._api_kwargs,
        )
