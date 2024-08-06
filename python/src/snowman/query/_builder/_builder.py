from abc import ABC, abstractmethod
from typing import Any, NamedTuple

from snowman._features import USE_TURU, TuruSnowflakeCursor
from snowman.cursor import Cursor


class QueryWithParams(NamedTuple):
    query: str
    params: tuple[Any, ...]


class QueryBuilder(ABC):
    @abstractmethod
    def build(self) -> QueryWithParams: ...

    @abstractmethod
    def execute(self, cursor: Cursor, /) -> None: ...


def execute_with_tag(
    tag,
    cursor: Cursor,
    query: str,
    params: tuple[Any, ...],
):
    if USE_TURU and isinstance(cursor, TuruSnowflakeCursor):
        cursor.execute_with_tag(tag, query, params)

    else:
        cursor.execute(query, params)


def executemany_with_tag(
    tag,
    cursor: Cursor,
    query: str,
    params: tuple[Any, ...],
):
    if USE_TURU and isinstance(cursor, TuruSnowflakeCursor):
        cursor.executemany_with_tag(tag, query, params)

    else:
        cursor.executemany(query, params)
