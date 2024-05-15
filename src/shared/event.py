from abc import ABC, abstractmethod


class Event:
    pass


class EventHandler(ABC):
    @abstractmethod
    async def handle(self, event: Event) -> None:
        raise NotImplementedError
