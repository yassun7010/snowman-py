from typing import Generic, Type

from typing_extensions import override

from snowman._cursor import Cursor
from snowman._features import TruncateTag
from snowman.relation import full_table_name
from snowman.relation.table import GenericTable

from ._builder import QueryBuilder, QueryWithParams, execute_with_tag


class TruncateQueryBuilder:
    @property
    def table(self) -> "TruncateTableStatement":
        return TruncateTableStatement()

    def __call__(
        self, table: Type[GenericTable], /
    ) -> "TruncateTableQueryBuilder[GenericTable]":
        return TruncateTableQueryBuilder(table, if_exists=False)

    @property
    def if_(self) -> "TruncateTableIfStatement":
        return TruncateTableIfStatement()


class TruncateTableStatement:
    def __call__(
        self, table: Type[GenericTable], /
    ) -> "TruncateTableQueryBuilder[GenericTable]":
        return TruncateTableQueryBuilder(table, if_exists=False)

    @property
    def if_(self) -> "TruncateTableIfStatement":
        return TruncateTableIfStatement()


class TruncateTableIfStatement:
    def exists(
        self, table: Type[GenericTable], /
    ) -> "TruncateTableQueryBuilder[GenericTable]":
        return TruncateTableQueryBuilder(table, if_exists=True)


class TruncateTableQueryBuilder(QueryBuilder[None], Generic[GenericTable]):
    def __init__(self, table: Type[GenericTable], /, *, if_exists: bool):
        self._table = table
        self._if_exists = if_exists

    @override
    def build(self) -> QueryWithParams:
        if_exists = " IF EXISTS" if self._if_exists else ""
        query = f"TRUNCATE TABLE{if_exists} {full_table_name(self._table)}"

        return QueryWithParams(query, ())

    @override
    def execute(self, cursor: Cursor) -> None:
        query, params = self.build()
        execute_with_tag(
            TruncateTag[self._table],  # type: ignore
            cursor,
            query,
            params,
        )
