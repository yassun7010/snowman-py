import itertools
from typing import Any, Generic, Sequence, Type, cast

from pydantic import BaseModel
from typing_extensions import override

from snowman.relation import full_table_name
from snowman.relation.table import GenericTable, GenericUpdateColumnTypedDict

from ._builder import QueryBuilder, QueryWithParams


class UpdateStatement(Generic[GenericTable, GenericUpdateColumnTypedDict]):
    def __init__(
        self,
        table: Type[GenericTable],
        /,
        *,
        _columns_type: Type[GenericUpdateColumnTypedDict] | None = None,
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

    def where(
        self,
        condition: str,
        params: Sequence[Any] | None = None,
        /,
    ) -> "UpdateSetWhereQueryBuidler":
        """
        Specify the condition of the where clause.

        Query parameters only support positional placeholders, so specify them with `%s`.

        e.g)
            `.where("id = %s AND name = %s", [1, "Alice"])`
        """
        return UpdateSetWhereQueryBuidler(
            self._table,
            self._columns,
            where_condition=condition,
            where_params=params or (),
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
        where_params: Sequence[Any],
    ):
        self._table = table
        self._columns = cast(
            dict,
            columns.model_dump(exclude_unset=True)
            if isinstance(columns, BaseModel)
            else columns,
        )
        self._where_condition = where_condition
        self._where_params = where_params

    @override
    def build(self) -> QueryWithParams:
        values = ",\n    ".join([f"{key} = %s" for key in self._columns.keys()])

        query = f"""
UPDATE
    {full_table_name(self._table)}
SET
    {values}
WHERE
    {self._where_condition}
""".strip()

        return QueryWithParams(
            query,
            tuple(itertools.chain(self._columns.values(), self._where_params)),
        )
