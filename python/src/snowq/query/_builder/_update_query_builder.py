from typing import Generic, Type, cast

from pydantic import BaseModel
from typing_extensions import override

from snowq.relation import full_table_name
from snowq.relation.table import GenericTable, GenericUpdateColumnTypedDict

from ._builder import QueryBuilder, QueryWithParams


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
        table: Type[GenericTable],
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
    def build(self) -> QueryWithParams:
        values = ",\n    ".join([f"{key} = %({key})s" for key in self._columns.keys()])

        query = f"""
UPDATE
    {full_table_name(self._table)}
SET
    {values}
WHERE
    {self._where_condition}
""".strip()

        return QueryWithParams(query, {k: v for k, v in self._columns.items()})
