import asyncio
from functools import wraps
from typing import (
    TypeVar,
    ParamSpec,
    Callable,
    Type,
    Optional,
    Union,
    Tuple,
    Any,
    Coroutine,
    overload,
)

P = ParamSpec('P')  # Параметры оригинальной функции
R = TypeVar('R')  # Возвращаемый тип оригинальной функции


@overload
def retry(
    func: Callable[P, Coroutine[Any, Any, R]],
) -> Callable[P, Coroutine[Any, Any, R]]: ...


@overload
def retry(
    *,
    max_retries: int = 3,
    delay: Union[float, int] = 1,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
    on_retry: Optional[Callable[[int, Exception], None]] = None,
) -> Callable[[Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]]: ...


def retry(
    func: Optional[Callable[P, Coroutine[Any, Any, R]]] = None,
    *,
    max_retries: int = 3,
    delay: Union[float, int] = 1,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
    on_retry: Optional[Callable[[int, Exception], None]] = None,
) -> Union[
    Callable[P, Coroutine[Any, Any, R]],
    Callable[[Callable[P, Coroutine[Any, Any, R]]], Callable[P, Coroutine[Any, Any, R]]],
]:
    """
    Декоратор для повторного выполнения асинхронной функции при ошибках.

    Args:
        func: func for retry
        max_retries: Максимальное количество попыток (по умолчанию 3).
        delay: Задержка между попытками в секундах (по умолчанию 1).
        exceptions: Типы исключений, при которых нужно повторять (по умолчанию все).
        on_retry: Функция для логирования/обработки попытки (attempt, error).

    Returns:
        Декорированную асинхронную функцию с поддержкой повторных попыток.
    """

    def decorator(f: Callable[P, Coroutine[Any, Any, R]]) -> Callable[P, Coroutine[Any, Any, R]]:
        @wraps(f)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_error: Optional[Exception] = None
            for attempt in range(1, max_retries + 1):
                try:
                    return await f(*args, **kwargs)
                except exceptions as e:
                    last_error = e
                    if on_retry:
                        on_retry(attempt, e)
                    if attempt < max_retries:
                        await asyncio.sleep(delay)
            raise last_error if last_error else RuntimeError('Неизвестная ошибка')

        return wrapper

    if func is not None:
        return decorator(func)
    return decorator
