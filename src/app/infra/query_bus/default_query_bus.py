from src.app.domain import QueryBus, QueryDoesNotHaveHandlerException
from src.shared import DataType, Query, QueryHandler, QueryResponse


class DefaultQueryBus(QueryBus[DataType]):
    def __init__(self, handlers: dict[type[Query], QueryHandler]):
        self.handlers = handlers

    async def dispatch(self, query: Query) -> QueryResponse[DataType]:
        if handler := self.handlers.get(type(query)):
            return await handler.handle(query)

        raise QueryDoesNotHaveHandlerException()
