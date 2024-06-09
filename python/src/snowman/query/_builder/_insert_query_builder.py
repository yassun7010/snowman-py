from typing import Generic, Sequence, Type

from typing_extensions import override

import snowman._features
from snowman.cursor import Cursor, _get_snowflake_connection
from snowman.exception import snowmanNotDataFrameAvailableError
from snowman.relation import full_table_name, table_column_names, table_columns_dict
from snowman.relation.table import (
    GenericInsertColumnTypedDict,
    GenericTable,
    GenericUpdateColumnTypedDict,
    Table,
)

from ._builder import QueryBuilder, QueryWithParams


class InsertQueryBuilder:
    """
    Insert records into a table.

    >>> from snowman.query import insert
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
    (
        id,
        name
    )
    VALUES (
        %s,
        %s
    )
    """

    @property
    def overwrite(self) -> "InsertOverwriteQueryBuilder":
        return InsertOverwriteQueryBuilder()

    def into(
        self,
        table: Type[Table[GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]],
        /,
    ):
        return InsertIntoQueryBuilder(
            table,
            _columns_type=table.__insert_columns__,  # type: ignore
        )


class InsertOverwriteQueryBuilder:
    def into(
        self,
        table: Type[Table[GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]],
        /,
    ):
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
        _columns_type: Type[GenericInsertColumnTypedDict] | None,
    ) -> None:
        self._table = table
        self._overwrite = overwtire

    def values(
        self,
        values: GenericTable
        | GenericInsertColumnTypedDict
        | Sequence[GenericTable | GenericInsertColumnTypedDict]
        | snowman._features.PandasDataFrame,
        /,
    ) -> "InsertIntoValuesQueryBuilder[GenericTable, GenericInsertColumnTypedDict]":
        if isinstance(values, snowman._features.PandasDataFrame):
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
        dataframe: snowman._features.PandasDataFrame | None = None,
        overwrite: bool = False,
    ):
        self._table = table
        self._values = values
        self._dataframe = dataframe
        self._overwrite = overwrite
        self._use_execute_many = len(values) != 1

    @override
    def build(self) -> QueryWithParams:
        if self._dataframe is not None:
            raise snowmanNotDataFrameAvailableError()

        overwrite = "OVERWRITE " if self._overwrite else ""
        names = table_column_names(self._table)
        keys = ",\n    ".join(names)
        values = ",\n    ".join("%s" for _ in names)

        query = f"""
INSERT {overwrite}INTO
    {full_table_name(self._table)}
(
    {keys}
)
VALUES (
    {values}
)
""".strip()

        return QueryWithParams(
            query,
            (
                tuple(
                    tuple(table_columns_dict(value).values()) for value in self._values
                )
                if self._use_execute_many
                else tuple(table_columns_dict(self._values[0]).values())
            ),
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

        elif self._use_execute_many:
            cursor.executemany(*self.build())

        else:
            cursor.execute(*self.build())
