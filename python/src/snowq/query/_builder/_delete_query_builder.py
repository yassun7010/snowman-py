from typing import Generic, Type
from typing_extensions import override

from snowq.relation import full_table_name
from snowq.relation.table import GenericTable

from ._builder import QueryBuilder, QueryWithParams


class DeleteQueryBuilder:
    def from_(self, table: Type[GenericTable]) -> "DeleteFromStatement[GenericTable]":
        return DeleteFromStatement(table)


class DeleteFromStatement(Generic[GenericTable]):
    def __init__(self, table: Type[GenericTable]):
        self._table = table

    def where(self, condition: str) -> "UpdateFromWhereQueryBuilder[GenericTable]":
        return UpdateFromWhereQueryBuilder(self._table, condition)


class UpdateFromWhereQueryBuilder(Generic[GenericTable], QueryBuilder):
    def __init__(self, table: Type[GenericTable], where_condition: str):
        self._table = table
        self._where_condition = where_condition

    @override
    def build(self) -> QueryWithParams:
        query = f"""
DELETE FROM
    {full_table_name(self._table)}
WHERE
    {self._where_condition}
""".strip()

        return QueryWithParams(query, {})
