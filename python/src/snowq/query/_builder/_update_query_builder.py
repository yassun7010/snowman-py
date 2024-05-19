from typing import Generic, Type, cast

from pydantic import BaseModel
from typing_extensions import override

from snowq.schema import GenericTablable, full_name
from snowq.schema.table import GenericUpdateColumnTypedDict

from ._builder import QueryBuilder, QueryParams


class UpdateStatement(Generic[GenericTablable, GenericUpdateColumnTypedDict]):
    def __init__(
        self,
        table: Type[GenericTablable],
        _columns_type: GenericUpdateColumnTypedDict | None = None,
    ) -> None:
        self._table = table

    def set(
        self,
        fields: GenericTablable | GenericUpdateColumnTypedDict,
    ) -> "UpdateSetQueryBuilder[GenericTablable, GenericUpdateColumnTypedDict]":
        return UpdateSetQueryBuilder(self._table, fields)


class UpdateSetQueryBuilder(
    Generic[GenericTablable, GenericUpdateColumnTypedDict], QueryBuilder
):
    def __init__(
        self,
        table: type[GenericTablable],
        columns: GenericTablable | GenericUpdateColumnTypedDict,
    ):
        self._table = table
        self._columns = cast(
            dict,
            columns.model_dump(exclude_unset=True)
            if isinstance(columns, BaseModel)
            else columns,
        )

    @override
    def build(self) -> QueryParams:
        query = f"""
UPDATE
    {full_name(self._table)}
SET
    {',\n    '.join([f'{key} = %({key})s' for key in self._columns.keys()])}
""".strip()

        return QueryParams(query, {k: v for k, v in self._columns.items()})
