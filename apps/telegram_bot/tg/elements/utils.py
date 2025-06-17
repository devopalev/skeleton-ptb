import typing
from abc import ABC, abstractmethod


class BaseCallbackConstructor(ABC):
    @classmethod
    @abstractmethod
    def from_callback_data(cls, callback_data: str) -> 'BaseCallbackConstructor': ...

    @property
    @abstractmethod
    def callback_data(self) -> str: ...

    def __str__(self) -> str:
        return self.callback_data


class CallbackBuilder(BaseCallbackConstructor):
    splitter = ':'

    def __init__(self, *callback: str) -> None:
        self._elements = callback

    def __str__(self) -> str:
        return self.callback_data

    def __eq__(self, other: typing.Any) -> bool:
        return isinstance(other, CallbackBuilder) and self.callback_data == other.callback_data

    def add_callback(self, callback: str) -> 'CallbackBuilder':
        return self.__class__(str(self), callback)

    def issubset(self, other: 'CallbackBuilder') -> bool:
        if not isinstance(other, CallbackBuilder):
            raise TypeError('Unknown type')
        return set(self._elements).issubset(set(other._elements))

    @property
    def callback_data(self) -> str:
        return self.splitter.join(self._elements)

    @property
    def callback_rejex(self) -> str:
        return '^' + self.callback_data + '$'

    @classmethod
    def from_callback_data(cls, callback_data: str) -> 'CallbackBuilder':
        return cls(*callback_data.split(cls.splitter))

    @property
    def last_element(self) -> str:
        return self._elements[-1]
