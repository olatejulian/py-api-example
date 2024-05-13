from abc import ABC, abstractmethod
from typing import Generic

from src.shared import DataType, Query, QueryResponse


class QueryDoesNotHaveHandlerException(Exception):
    pass


class QueryBus(ABC, Generic[DataType]):
    @abstractmethod
    async def dispatch(self, query: Query) -> QueryResponse[DataType]:
        raise NotImplementedError
