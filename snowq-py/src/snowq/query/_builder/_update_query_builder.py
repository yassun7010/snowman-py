from typing import Any, Generic, Type

from typing_extensions import override

from snowq.schema import GenericTablable, full_name

from ._builder import QueryBuilder, QueryParams


class UpdateStatement(Generic[GenericTablable]):
    def __init__(self, table: Type[GenericTablable]) -> None:
        self._table = table

    def set(self, **fields: Any) -> "UpdateSetQueryBuilder":
        return UpdateSetQueryBuilder(self._table, fields)


class UpdateSetQueryBuilder(Generic[GenericTablable], QueryBuilder):
    def __init__(self, table: type[GenericTablable], columns: dict[str, Any]):
        self._table = table
        self._columns = columns

    @override
    def build(self) -> QueryParams:
        query = f"""
UPDATE
    {full_name(self._table)}
SET
    {'\n    '.join([f'{key} = %({key})s' for key in self._columns.keys()])}
""".strip()

        return QueryParams(query, self._columns)
