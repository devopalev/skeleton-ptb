import abc
import itertools
import logging
import typing
from typing import Callable, Coroutine, Any, ParamSpec, TypeVar, Sequence

from telegram import BotCommand, Update
from telegram.ext import BaseHandler, ConversationHandler

from apps.telegram_bot import CustomContext
from apps.telegram_bot.core.custom_handlers import CommandHandlerCustom

P = ParamSpec('P')  # Параметры оригинальной функции
R = TypeVar('R')  # Возвращаемый тип оригинальной функции


class _BaseRouter(abc.ABC):
    @abc.abstractmethod
    def get_handlers(self) -> Sequence[BaseHandler[Update, CustomContext]]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_bot_commands(self) -> Sequence[BotCommand]:
        raise NotImplementedError


class ConversationRouter(_BaseRouter):
    def __init__(
        self,
        name: typing.Optional[str] = None,
        **conversation_options: dict[str, Any],
    ):
        super().__init__()
        self.name = name
        self._entrypoints: list[BaseHandler[Update, CustomContext]] = []
        self._states: dict[Any, list[BaseHandler[Update, CustomContext]]] = {}
        self._fallbacks: list[BaseHandler[Update, CustomContext]] = []
        self._options: dict[str, Any] = conversation_options
        self._logger = logging.getLogger(self.__class__.__name__)

    def get_bot_commands(self) -> Sequence[BotCommand]:
        commands = []
        for handler in self._entrypoints:
            if isinstance(handler, CommandHandlerCustom):
                if handler.show_command:
                    commands.append(handler.build_bot_command())
        return commands

    def get_handlers(self) -> Sequence[ConversationHandler[CustomContext]]:
        return (
            ConversationHandler(
                entry_points=self._entrypoints,
                states=self._states,
                fallbacks=self._fallbacks,
                **self._options,
            ),
        )

    def register_state(
        self,
        state: Any,
        class_handler: type[BaseHandler[Update, CustomContext]],
        **handler_options: Any,
    ) -> Callable[[Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]]:
        def decorator(
            callback: Callable[P, Coroutine[Any, Any, R]],
        ) -> Callable[P, Coroutine[Any, Any, R]]:
            handler = class_handler(callback=callback, **handler_options)  # type: ignore[arg-type]
            self._states.setdefault(state, []).append(handler)
            self._logger.info('Registered handler %s', handler)
            return callback

        return decorator

    def register_entrypoint(
        self,
        class_handler: type[BaseHandler[Update, CustomContext]],
        **handler_options: Any,
    ) -> Callable[[Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]]:
        def decorator(
            callback: Callable[P, Coroutine[Any, Any, R]],
        ) -> Callable[P, Coroutine[Any, Any, R]]:
            handler = class_handler(callback=callback, **handler_options)  # type: ignore[arg-type]
            self._entrypoints.append(handler)
            self._logger.info('Registered handler %s', handler)
            return callback

        return decorator

    def register_fallback(
        self,
        class_handler: type[BaseHandler[Update, CustomContext]],
        **handler_options: Any,
    ) -> Callable[[Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]]:
        def decorator(
            callback: Callable[P, Coroutine[Any, Any, R]],
        ) -> Callable[P, Coroutine[Any, Any, R]]:
            handler = class_handler(callback=callback, **handler_options)  # type: ignore[arg-type]
            self._fallbacks.append(handler)
            self._logger.info('Registered handler %s', handler)
            return callback

        return decorator


class Router(_BaseRouter):
    def __init__(self) -> None:
        super().__init__()
        self._handlers: list[BaseHandler[Update, CustomContext]] = []
        self._routers: list[_BaseRouter] = []
        self._conversations: dict[str, ConversationRouter] = {}
        self._logger = logging.getLogger(self.__class__.__name__)

    def get_handlers(self) -> list[BaseHandler[Any, Any]]:
        other_routers = list(itertools.chain.from_iterable(r.get_handlers() for r in self._routers))
        return other_routers + self._handlers

    def get_bot_commands(self) -> Sequence[BotCommand]:
        other_commands = list(itertools.chain.from_iterable(r.get_bot_commands() for r in self._routers))

        commands = []
        for handler in self._handlers:
            if isinstance(handler, CommandHandlerCustom):
                if handler.show_command:
                    commands.append(handler.build_bot_command())

        return commands + other_commands

    def add_router(
        self,
        router: _BaseRouter,
    ) -> None:
        self._routers.append(router)

    def register_handler(
        self,
        class_handler: type[BaseHandler[Update, CustomContext]],
        **handler_options: Any,
    ) -> Callable[[Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]]:
        def decorator(
            callback: Callable[P, Coroutine[Any, Any, R]],
        ) -> Callable[P, Coroutine[Any, Any, R]]:
            handler = class_handler(callback=callback, **handler_options)  # type: ignore[arg-type]
            self._handlers.append(handler)
            self._logger.info('Registered handler %s', handler)
            return callback

        return decorator


def register_state(
    routers: Sequence[ConversationRouter],
    state: Any,
    class_handler: type[BaseHandler[Update, CustomContext]],
    **handler_options: Any,
) -> Callable[[Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]]:
    def decorator(
        callback: Callable[P, Coroutine[Any, Any, R]],
    ) -> Callable[P, Coroutine[Any, Any, R]]:
        for router in routers:
            router.register_state(state, class_handler, **handler_options)(callback)
        return callback

    return decorator


def register_entrypoint(
    routers: Sequence[ConversationRouter],
    class_handler: type[BaseHandler[Update, CustomContext]],
    **handler_options: Any,
) -> Callable[[Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]]:
    def decorator(
        callback: Callable[P, Coroutine[Any, Any, R]],
    ) -> Callable[P, Coroutine[Any, Any, R]]:
        for router in routers:
            router.register_entrypoint(class_handler, **handler_options)(callback)
        return callback

    return decorator


def register_fallback(
    routers: Sequence[ConversationRouter],
    class_handler: type[BaseHandler[Update, CustomContext]],
    **handler_options: Any,
) -> Callable[[Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]]:
    def decorator(
        callback: Callable[P, Coroutine[Any, Any, R]],
    ) -> Callable[P, Coroutine[Any, Any, R]]:
        for router in routers:
            router.register_fallback(class_handler, **handler_options)(callback)
        return callback

    return decorator
