# pylint: disable=invalid-name
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

CommandType = TypeVar(
    "CommandType",
    bound="Command",
)

CommandHandlerResponseType = TypeVar(
    "CommandHandlerResponseType",
)


class CommandDoesNotHaveHandlerException(Exception):
    pass


class Command:
    pass


class CommandHandler(ABC):
    @abstractmethod
    async def handle(self, command: Command) -> Any:
        raise NotImplementedError


class CommandBus(ABC, Generic[CommandType, CommandHandlerResponseType]):
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
    async def dispatch(self, command: CommandType) -> CommandHandlerResponseType:
        raise NotImplementedError
