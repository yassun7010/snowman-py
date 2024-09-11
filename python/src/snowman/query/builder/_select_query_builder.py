from typing import Any, Callable, Generic, Sequence, Type, cast, overload

from typing_extensions import override

from snowman._cursor import Cursor
from snowman.query.builder.condition.condition import Condition
from snowman.query.builder.context import WhereContext
from snowman.relation import full_table_name
from snowman.relation.table import (
    GenericColumnAccessor,
    GenericInsertColumnTypedDict,
    GenericTable,
    GenericUpdateColumnTypedDict,
    Table,
)

from ._builder import QueryBuilder, QueryWithParams, execute


class SelectQueryBuilder:
    def __init__(self):
        pass

    def from_(
        self,
        table: Type[
            Table[
                GenericTable,
                GenericColumnAccessor,
                GenericInsertColumnTypedDict,
                GenericUpdateColumnTypedDict,
            ]
        ],
        /,
    ) -> "SelectFromStatement[GenericTable, GenericColumnAccessor, GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]":
        return SelectFromStatement(table)


class SelectFromStatement(
    QueryBuilder[
        "SelectCursor[GenericTable, GenericColumnAccessor, GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]"
    ],
    Generic[
        GenericTable,
        GenericColumnAccessor,
        GenericInsertColumnTypedDict,
        GenericUpdateColumnTypedDict,
    ],
):
    def __init__(
        self,
        table: Type[
            Table[
                GenericTable,
                GenericColumnAccessor,
                GenericInsertColumnTypedDict,
                GenericUpdateColumnTypedDict,
            ]
        ],
    ):
        self._table = table

    @overload
    def where(
        self,
        condition: Callable[[WhereContext[GenericColumnAccessor]], Condition],
        /,
    ) -> "SelectWhereQueryBuilder": ...

    @overload
    def where(
        self,
        condition: Condition,
        /,
    ) -> "SelectWhereQueryBuilder": ...

    @overload
    def where(
        self,
        condition: str,
        params: Sequence[Any] | None = None,
        /,
    ) -> "SelectWhereQueryBuilder": ...

    def where(
        self,
        condition: Callable[[WhereContext[GenericColumnAccessor]], Condition]
        | Condition
        | str,
        params: Sequence[Any] | None = None,
        /,
    ) -> "SelectWhereQueryBuilder":
        if callable(condition):
            condition, params = condition(WhereContext(self._table)).to_sql()
        elif isinstance(condition, Condition):
            condition, params = condition.to_sql()

        return SelectWhereQueryBuilder(self._table, condition, params or ())

    @override
    def build(self) -> QueryWithParams:
        return QueryWithParams(
            f"""
SELECT
    *
FROM
    {full_table_name(self._table)}
""".strip(),
            (),
        )

    @override
    def execute(
        self, cursor: Cursor
    ) -> "SelectCursor[GenericTable, GenericColumnAccessor, GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]":
        query, params = self.build()
        print(query)

        return SelectCursor(execute(cursor, query, params), self._table)


class SelectWhereQueryBuilder(
    QueryBuilder[
        "SelectCursor[GenericTable, GenericColumnAccessor, GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]"
    ],
    Generic[
        GenericTable,
        GenericColumnAccessor,
        GenericInsertColumnTypedDict,
        GenericUpdateColumnTypedDict,
    ],
):
    def __init__(
        self,
        table: Type[
            Table[
                GenericTable,
                GenericColumnAccessor,
                GenericInsertColumnTypedDict,
                GenericUpdateColumnTypedDict,
            ]
        ],
        where_condition: str,
        where_params: Sequence[Any],
    ):
        self._table = table
        self._where_condition = where_condition
        self._where_params = where_params

    @override
    def build(self) -> QueryWithParams:
        query = f"""
SELECT
    *
FROM
    {full_table_name(self._table)}
WHERE
    {self._where_condition}
""".strip()

        return QueryWithParams(query, tuple(self._where_params))

    @override
    def execute(
        self, cursor: Cursor
    ) -> "SelectCursor[GenericTable, GenericColumnAccessor, GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]":
        query, params = self.build()

        return SelectCursor(execute(cursor, query, params), self._table)


class SelectCursor(
    Generic[
        GenericTable,
        GenericColumnAccessor,
        GenericInsertColumnTypedDict,
        GenericUpdateColumnTypedDict,
    ]
):
    def __init__(
        self,
        cursor: Cursor,
        table: Type[
            Table[
                GenericTable,
                GenericColumnAccessor,
                GenericInsertColumnTypedDict,
                GenericUpdateColumnTypedDict,
            ]
        ],
    ):
        self._cursor = cursor

    def fetchall(self) -> list[GenericColumnAccessor]:
        return cast(list[GenericColumnAccessor], self._cursor.fetchall())
