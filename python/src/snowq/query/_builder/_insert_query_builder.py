from typing import Generic, Sequence, Type

from typing_extensions import override

import snowq._features
from snowq.cursor import Cursor, _get_snowflake_connection
from snowq.exception import SnowqNotDataFrameAvailableError
from snowq.relation import column_names, columns_dict, full_table_name
from snowq.relation.table import (
    GenericInsertColumnTypedDict,
    GenericTable,
    GenericUpdateColumnTypedDict,
    Table,
)

from ._builder import QueryBuilder, QueryWithParams


class InsertQueryBuilder:
    """
    Insert records into a table.

    >>> from snowq.query import insert
    >>> from your.database.schema import User
    >>>
    >>> query, _ = (
    ...     insert.into(
    ...         User
    ...     ).values(
    ...         {"id": 1, "name": "Alice"}
    ...     )
    ... ).build()
    >>>
    >>> print(query)
    INSERT INTO
        database.schema.users
    VALUES (
        %(id)s,
        %(name)s
    )
    """

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
        | Sequence[GenericTable | GenericInsertColumnTypedDict]
        | snowq._features.PandasDataFrame,
    ) -> "InsertIntoValuesQueryBuilder[GenericTable, GenericInsertColumnTypedDict]":
        if isinstance(values, snowq._features.PandasDataFrame):
            dataframe = values
            values = ()

        else:
            dataframe = None
            if not isinstance(values, Sequence):
                values = (values,)

        return InsertIntoValuesQueryBuilder(
            self._table,
            values,
            dataframe=dataframe,
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
        *,
        dataframe: snowq._features.PandasDataFrame | None = None,
        overwrite: bool = False,
    ):
        self._table = table
        self._values = values
        self._dataframe = dataframe
        self._overwrite = overwrite

    @override
    def build(self) -> QueryWithParams:
        if self._dataframe is not None:
            raise SnowqNotDataFrameAvailableError()

        overwrite = "OVERWRITE " if self._overwrite else ""
        values = ",\n    ".join(
            [f"%({column_name})s" for column_name in column_names(self._table)]
        )

        query = f"""
INSERT {overwrite}INTO
    {full_table_name(self._table)}
VALUES (
    {values}
)
""".strip()

        return QueryWithParams(
            query,
            columns_dict(self._values[0])
            if len(self._values) == 1
            else tuple(columns_dict(value) for value in self._values),
        )

    @override
    def execute(self, cursor: Cursor, /) -> None:
        if self._dataframe is not None:
            from snowflake.connector.pandas_tools import write_pandas

            write_pandas(
                conn=_get_snowflake_connection(cursor),
                df=self._dataframe,
                table_name=self._table.__table_name__,
                database=self._table.__databas_name__,
                schema=self._table.__schema_name__,
            )
            return

        else:
            super().execute(cursor)
