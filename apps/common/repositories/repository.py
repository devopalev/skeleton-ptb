from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    async def get(self) -> None: ...

    @abstractmethod
    async def get_list(self) -> None: ...

    @abstractmethod
    async def create(self) -> None: ...

    @abstractmethod
    async def delete(self) -> None: ...


class Repository(AbstractRepository):
    async def get(self) -> None:
        raise NotImplementedError()

    async def get_list(self) -> None:
        raise NotImplementedError()

    async def create(self) -> None:
        raise NotImplementedError()

    async def delete(self) -> None:
        raise NotImplementedError()


##############################################
# Simple approach to the repository
##############################################


async def get() -> None:
    # conn = await db.connection()
    raise NotImplementedError()


async def get_list() -> None:
    # conn = await db.connection()
    raise NotImplementedError()


async def create() -> None:
    # conn = await db.connection()
    raise NotImplementedError()


async def delete() -> None:
    # conn = await db.connection()
    raise NotImplementedError()
