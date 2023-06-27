from src.shared.celery import event_handler_task
from src.shared.interface import Event, EventBus, EventDoesNotHaveHandlersException


class CeleryEventBus(EventBus):
    async def dispatch(self, event: Event) -> None:
        event_name = event.get_event_name()

        if event_name not in self._handlers:
            raise EventDoesNotHaveHandlersException()

        handlers = self._handlers[event_name]

        for handler in handlers:
            event_handler_task.apply_async(
                kwargs={"handler": handler, "event": event}  # type: ignore
            )
