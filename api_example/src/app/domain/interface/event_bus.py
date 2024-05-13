from abc import ABC, abstractmethod

from ....shared.event import Event, EventHandler


class EventDoesNotHaveHandlersException(Exception):
    pass


class EventBus(ABC):
    def __init__(self, handlers: dict[type[Event], list[EventHandler]]):
        self.handlers = handlers

    @abstractmethod
    async def dispatch(self, event: Event) -> None:
        raise NotImplementedError
