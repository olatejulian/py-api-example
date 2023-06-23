# pylint: disable=invalid-name
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TCommand = TypeVar(
    "TCommand",
    bound="Command",
)


class CommandDoesNotHaveHandlerException(Exception):
    pass


class Command:
    pass


class CommandHandler(ABC, Generic[TCommand]):
    @abstractmethod
    async def handle(self, command: TCommand) -> None:
        raise NotImplementedError


class CommandBus(ABC):
    @abstractmethod
    def register(
        self,
        command_class: type[Command],
        handler: CommandHandler,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def register_many(
        self,
        commands_and_handlers: dict[type[Command], CommandHandler],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def dispatch(self, command: Command) -> None:
        raise NotImplementedError
