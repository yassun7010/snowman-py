from typing import Generic, Type

from typing_extensions import override

from snowman.relation import full_table_name
from snowman.relation.table import GenericTable

from ._builder import QueryBuilder, QueryWithParams


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


class TruncateTableQueryBuilder(Generic[GenericTable], QueryBuilder):
    def __init__(self, table: Type[GenericTable], /, *, if_exists: bool):
        self._table = table
        self._if_exists = if_exists

    @override
    def build(self) -> QueryWithParams:
        query = f"TRUNCATE TABLE{ ' IF EXISTS' if self._if_exists else ''} {full_table_name(self._table)}"

        return QueryWithParams(query, ())
