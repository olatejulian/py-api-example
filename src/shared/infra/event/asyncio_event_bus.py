import asyncio

from src.shared.interface import Event, EventBus, EventDoesNotHaveHandlersException


class AsyncioEventBus(EventBus):
    async def dispatch(self, event: Event) -> None:
        event_name = event.get_event_name()

        if event_name not in self._handlers:
            raise EventDoesNotHaveHandlersException()

        handlers = self._handlers[event_name]

        tasks = [handler.handle(event) for handler in handlers]

        await asyncio.gather(*tasks)
