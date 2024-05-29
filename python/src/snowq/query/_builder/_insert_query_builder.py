from typing import Generic, Sequence, Type

from typing_extensions import override

from snowq.schema import column_names, columns_dict, full_table_name
from snowq.schema.table import (
    GenericInsertColumnTypedDict,
    GenericTable,
    GenericUpdateColumnTypedDict,
    Table,
)

from ._builder import QueryBuilder, QueryWithParams


class InsertQueryBuilder:
    @property
    def overwrite(self) -> "InsertOverwriteQueryBuilder":
        return InsertOverwriteQueryBuilder()

    def into(
        self,
        table: Type[Table[GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]],
    ):
        return InsertIntoQueryBuilder(
            table,
            _columns_type=table.__insert_columns__,  # type: ignore
        )


class InsertOverwriteQueryBuilder:
    def into(self, table: Type[GenericTable]) -> "InsertIntoQueryBuilder":
        return InsertIntoQueryBuilder(
            table,
            overwtire=True,
            _columns_type=table.__insert_columns__,  # type: ignore
        )


class InsertIntoQueryBuilder(Generic[GenericTable, GenericInsertColumnTypedDict]):
    def __init__(
        self,
        table: Type[GenericTable],
        *,
        overwtire: bool = False,
        _columns_type: GenericInsertColumnTypedDict | None,
    ) -> None:
        self._table = table
        self._overwrite = overwtire

    def values(
        self,
        values: GenericTable
        | GenericInsertColumnTypedDict
        | Sequence[GenericTable | GenericInsertColumnTypedDict],
    ) -> "InsertIntoValuesQueryBuilder[GenericTable, GenericInsertColumnTypedDict]":
        values = values if isinstance(values, Sequence) else (values,)
        return InsertIntoValuesQueryBuilder(
            self._table,
            values if isinstance(values, Sequence) else (values,),
            overwrite=self._overwrite,
        )


class InsertIntoValuesQueryBuilder(
    Generic[GenericTable, GenericInsertColumnTypedDict], QueryBuilder
):
    def __init__(
        self,
        table: type[GenericTable],
        values: Sequence[GenericTable | GenericInsertColumnTypedDict],
        /,
        overwrite: bool = False,
    ):
        self._table = table
        self._values = values
        self._overwrite = overwrite

    @override
    def build(self) -> QueryWithParams:
        overwrite = "OVERWRITE " if self._overwrite else ""
        query = f"""
INSERT {overwrite}INTO
    {full_table_name(self._table)}
VALUES (
    {',\n    '.join([f'%({column_name})s' for column_name in column_names(self._table)])}
)
""".strip()

        return QueryWithParams(
            query,
            columns_dict(self._values[0])
            if len(self._values) == 1
            else tuple(columns_dict(value) for value in self._values),
        )
