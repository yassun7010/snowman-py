from abc import ABC, abstractmethod
from typing import Any, Generic, NamedTuple, TypeVar

from snowman._cursor import Cursor
from snowman._features import USE_TURU, TuruSnowflakeCursor

GenericExecuteResult = TypeVar("GenericExecuteResult")


class QueryWithParams(NamedTuple):
    query: str
    params: tuple[Any, ...]


class QueryBuilder(Generic[GenericExecuteResult], ABC):
    @abstractmethod
    def build(self) -> QueryWithParams: ...

    @abstractmethod
    def execute(self, cursor: Cursor, /) -> GenericExecuteResult: ...


def execute(cursor: Cursor, query: str, params: tuple[Any, ...]):
    cursor.execute(query, params)

    return cursor


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
