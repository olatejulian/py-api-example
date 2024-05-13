from src.shared import Entity, Event


class SimpleEvent(Event):
    pass


class SimpleEntity(Entity):
    def __init__(self):
        self._events = []
        self._add_event(SimpleEvent())


def test_entity_collect_events():
    entity = SimpleEntity()

    events = list(entity.collect_events())

    assert len(events) == 1
