from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TEvent = TypeVar("TEvent", bound="Event")  # pylint: disable=invalid-name


class EventDoesNotHaveHandlersException(Exception):
    pass


class Event(ABC):
    @classmethod
    @abstractmethod
    def get_event_name(cls) -> str:
        raise NotImplementedError


class EventHandler(ABC, Generic[TEvent]):
    @abstractmethod
    async def handle(self, event: TEvent) -> None:
        raise NotImplementedError


class EventBus(ABC):
    _handlers: dict[str, list[EventHandler]]

    def __init__(self):
        self._handlers = {}

    def register(
        self,
        event: type[Event],
        handler: EventHandler,
    ) -> None:
        event_name = event.get_event_name()

        if event_name not in self._handlers:
            self._handlers[event_name] = []

        self._handlers[event_name].append(handler)

    def register_many(
        self,
        events_and_handlers: dict[type[Event], list[EventHandler]],
    ) -> None:
        for event, handlers in events_and_handlers.items():
            for handler in handlers:
                self.register(event, handler)

    @abstractmethod
    async def dispatch(self, event: Event) -> None:
        raise NotImplementedError
