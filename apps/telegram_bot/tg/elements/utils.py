import typing


class CallbackManager:
    _symbol_slitter = '?'
    _symbol_elements = '&'
    _symbol_values = '='
    _symbol_list = ','
    _key_values = 'values[]'

    def __init__(
        self,
        path: str,
        *args: str,
        **kwargs: str,
    ):
        self.path = path
        self.args: list[str] = list(args) or []
        self.kwargs: dict[str, str] = kwargs or {}

    def __str__(self) -> str:
        result = f'{self.path}'
        arguments = ''

        if self.args:
            arguments += self._key_values + self._symbol_values + self._symbol_list.join(map(str, self.args))

        if self.kwargs:
            arguments += self._symbol_elements.join(map(lambda x: self._symbol_values.join(x), self.kwargs.items()))

        if arguments:
            result += self._symbol_slitter + arguments

        if (size := len(result.encode('utf-8'))) > 64:
            raise ValueError(f'The maximum size has been exceeded, got {size}, expected 64 bytes: {result}')

        return result

    @classmethod
    def deserialize(cls, data: str) -> 'CallbackManager':
        values, kwargs = [], {}
        if cls._symbol_slitter in data:
            path, parameters = data.split(cls._symbol_slitter)
        else:
            path, parameters = data, None

        if parameters:
            kwargs.update(dict(map(lambda x: x.split(cls._symbol_values), parameters.split(cls._symbol_elements))))

            if cls._key_values in kwargs:
                values.extend(kwargs.pop(cls._key_values).split(cls._symbol_list))

        return cls(path, *values, **kwargs)

    def add(self, *args: str, **kwargs: str) -> typing.Self:
        kwargs.update(self.kwargs)
        return self.__class__(self.path, *(list(args) + self.args), **kwargs)

    @property
    def last_value(self) -> typing.Optional[str]:
        if self.args:
            return self.args[-1]
        if self.kwargs:
            return tuple(self.kwargs.values())[-1]
        return None

    @property
    def rejex(self) -> str:
        return f'^{self}$'
