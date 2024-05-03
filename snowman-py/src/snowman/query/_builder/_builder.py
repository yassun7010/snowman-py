from abc import ABC, abstractmethod
from typing import Any, NamedTuple

from snowman.cursor import Cursor


class QueryParams(NamedTuple):
    query: str
    params: dict[str, Any]


class QueryBuilder(ABC):
    @abstractmethod
    def build(self) -> QueryParams: ...

    def execute(self, cursor: Cursor, /) -> None:
        query, params = self.build()
        cursor.execute(query, params)
