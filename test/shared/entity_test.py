from src.shared import Entity, Event

EVENT_NAME = "entity.created"


class SimpleEvent(Event):
    __event_name = EVENT_NAME

    @classmethod
    def get_event_name(cls) -> str:
        return cls.__event_name


class SimpleEntity(Entity):
    def __init__(self):
        self._events = []
        self._add_event(SimpleEvent())


def test_entity_collect_events():
    entity = SimpleEntity()
    events = list(entity.collect_events())
    assert len(events) == 1
    assert events[0].get_event_name() == EVENT_NAME
