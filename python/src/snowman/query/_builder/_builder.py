from abc import ABC, abstractmethod
from typing import Any, NamedTuple

from snowman.cursor import Cursor


class QueryWithParams(NamedTuple):
    query: str
    params: tuple[Any, ...]


class QueryBuilder(ABC):
    @abstractmethod
    def build(self) -> QueryWithParams: ...

    def execute(self, cursor: Cursor, /) -> None:
        query, params = self.build()

        cursor.execute(query, params)
