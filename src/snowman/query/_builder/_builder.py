from abc import ABC, abstractmethod
from typing import NamedTuple

from snowman.protocol.connection import Connection


class QueryParams(NamedTuple):
    query: str
    params: dict[str, str]


class QueryBuilder(ABC):
    @abstractmethod
    def build(self) -> QueryParams: ...

    def execute(self, conn: Connection) -> None:
        query, params = self.build()
        conn.execute(query, params)
