from typing import Any, Generic, Sequence, Type

from typing_extensions import override

from snowman.relation import full_table_name
from snowman.relation.table import GenericTable

from ._builder import QueryBuilder, QueryWithParams


class DeleteQueryBuilder:
    def from_(
        self, table: Type[GenericTable], /
    ) -> "DeleteFromStatement[GenericTable]":
        return DeleteFromStatement(table)


class DeleteFromStatement(Generic[GenericTable]):
    def __init__(self, table: Type[GenericTable]):
        self._table = table

    def where(
        self,
        condition: str,
        params: Sequence[Any] | None = None,
        /,
    ) -> "UpdateFromWhereQueryBuilder[GenericTable]":
        """
        Specify the condition of the where clause.

        Query parameters only support positional placeholders, so specify them with `%s`.

        e.g)
            `.where("id = %s AND name = %s", [1, "Alice"])`
        """
        return UpdateFromWhereQueryBuilder(self._table, condition, params or ())


class UpdateFromWhereQueryBuilder(Generic[GenericTable], QueryBuilder):
    def __init__(
        self,
        table: Type[GenericTable],
        where_condition: str,
        where_params: Sequence[Any],
    ):
        self._table = table
        self._where_condition = where_condition
        self._where_params = where_params

    @override
    def build(self) -> QueryWithParams:
        query = f"""
DELETE FROM
    {full_table_name(self._table)}
WHERE
    {self._where_condition}
""".strip()

        return QueryWithParams(query, tuple(self._where_params))
