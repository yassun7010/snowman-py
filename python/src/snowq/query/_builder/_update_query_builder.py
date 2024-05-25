from typing import Generic, Type, cast

from pydantic import BaseModel
from typing_extensions import override

from snowq.schema import full_name
from snowq.schema.table import GenericTable, GenericUpdateColumnTypedDict

from ._builder import QueryBuilder, QueryParams


class UpdateStatement(Generic[GenericTable, GenericUpdateColumnTypedDict]):
    def __init__(
        self,
        table: Type[GenericTable],
        *,
        _columns_type: GenericUpdateColumnTypedDict | None = None,
    ) -> None:
        self._table = table

    def set(
        self,
        fields: GenericTable | GenericUpdateColumnTypedDict,
    ) -> "UpdateSetQueryBuilder[GenericTable, GenericUpdateColumnTypedDict]":
        return UpdateSetQueryBuilder(self._table, fields)


class UpdateSetQueryBuilder(Generic[GenericTable, GenericUpdateColumnTypedDict]):
    def __init__(
        self,
        table: type[GenericTable],
        columns: GenericTable | GenericUpdateColumnTypedDict,
    ):
        self._table = table
        self._columns = cast(
            dict,
            columns.model_dump(exclude_unset=True)
            if isinstance(columns, BaseModel)
            else columns,
        )

    def where(self, condition: str) -> "UpdateSetWhereQueryBuidler":
        return UpdateSetWhereQueryBuidler(
            self._table,
            self._columns,
            where_condition=condition,
        )


class UpdateSetWhereQueryBuidler(
    Generic[GenericTable, GenericUpdateColumnTypedDict], QueryBuilder
):
    def __init__(
        self,
        table: type[GenericTable],
        columns: GenericTable | GenericUpdateColumnTypedDict,
        *,
        where_condition: str,
    ):
        self._table = table
        self._columns = cast(
            dict,
            columns.model_dump(exclude_unset=True)
            if isinstance(columns, BaseModel)
            else columns,
        )
        self._where_condition = where_condition

    @override
    def build(self) -> QueryParams:
        query = f"""
UPDATE
    {full_name(self._table)}
SET
    {',\n    '.join([f'{key} = %({key})s' for key in self._columns.keys()])}
WHERE
    {self._where_condition}
""".strip()

        return QueryParams(query, {k: v for k, v in self._columns.items()})
