from typing import Generator

from .event import Event


class Entity:
    _events: list[Event]

    def _add_event(self, event: Event) -> None:
        self._events.append(event)

    def collect_events(self) -> Generator[Event, None, None]:
        while self._events:
            yield self._events.pop(0)
