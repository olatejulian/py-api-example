from src.core.shared.interface import Event, EventBus, EventHandler


class FakeEventBus(EventBus):
    def register(
        self,
        event: type[Event],
        handler: EventHandler,
    ) -> None:
        print("FakeEventBus: register", event, handler)

    def register_many(
        self,
        events_and_handlers: dict[type[Event], list[EventHandler]],
    ) -> None:
        print("FakeEventBus: register_many", events_and_handlers)

    async def dispatch(self, event: Event) -> None:
        print(f"FakeEventBus: {event.get_event_name()}")
