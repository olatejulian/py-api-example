import asyncio

from celery import shared_task

from src.shared.interface import (
    Event,
    EventBus,
    EventDoesNotHaveHandlersException,
    EventHandler,
)


@shared_task()
def executer(handler: EventHandler, event: Event) -> None:
    asyncio.run(handler.handle(event))


class CeleryEventBus(EventBus):
    async def dispatch(self, event: Event) -> None:
        event_name = event.get_event_name()

        if event_name not in self._handlers:
            raise EventDoesNotHaveHandlersException()

        handlers = self._handlers[event_name]

        for handler in handlers:
            executer.apply_async(kwargs={"handler": handler, "event": event})  # type: ignore
