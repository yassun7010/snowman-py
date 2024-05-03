from typing import Generic, Type

from typing_extensions import override

from snowman.schema import GenericTablable

from ._builder import QueryBuilder, QueryParams


class UpdateStatement(Generic[GenericTablable]):
    def __init__(self, table: Type[GenericTablable]) -> None:
        self._table = table

    def set(self, record: GenericTablable) -> "UpdateSetQueryBuilder":
        return UpdateSetQueryBuilder(self._table, record)


class UpdateSetQueryBuilder(Generic[GenericTablable], QueryBuilder):
    def __init__(self, table: type[GenericTablable], values: GenericTablable):
        self._table = table
        self._values = values

    @override
    def build(self) -> QueryParams:
        return QueryParams("", {})
