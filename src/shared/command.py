from abc import ABC, abstractmethod
from typing import Any


class Command:
    pass


class CommandHandler(ABC):
    @abstractmethod
    async def handle(self, command: Command) -> Any:
        raise NotImplementedError
