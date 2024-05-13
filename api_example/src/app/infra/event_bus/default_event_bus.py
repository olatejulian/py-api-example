import asyncio

from src.app.domain import Event, EventBus, EventDoesNotHaveHandlersException


class DefaultEventBus(EventBus):
    async def dispatch(self, event: Event) -> None:
        if handlers := self.handlers.get(type(event), None):
            tasks = [
                (asyncio.create_task(handler.handle(event))) for handler in handlers
            ]

            await asyncio.gather(*tasks)

        else:
            raise EventDoesNotHaveHandlersException(type(event))
