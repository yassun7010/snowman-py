from typing import Any, Callable, Generic, Sequence, Type, cast, overload

from typing_extensions import override

from snowman._cursor import Cursor
from snowman.query.builder.condition.condition import Condition
from snowman.query.builder.context.order_by_context import OrderByContext
from snowman.query.builder.context.where_context import WhereContext
from snowman.query.column import Column
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
    ) -> "SelectFromQueryBuilder[GenericTable, GenericColumnAccessor, GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]":
        return SelectFromQueryBuilder(table)


class SelectFinalQueryBuilder(
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
        *,
        where_condition: str | None = None,
        where_params: Sequence[Any] | None = None,
        order_by_condition: str | None = None,
        order_by_params: Sequence[Any] | None = None,
        limit: int | None = None,
    ):
        self._table = table
        self._where_condition = where_condition
        self._where_params = tuple(where_params) if where_params else ()
        self._order_by_condition = order_by_condition
        self._order_by_params = tuple(order_by_params) if order_by_params else ()
        self._limit = limit
        self._limit_params = (limit,) if limit is not None else ()

    @override
    def build(self) -> QueryWithParams:
        where_clause = (
            f" WHERE {self._where_condition}" if self._where_condition else ""
        )
        order_by_clause = (
            f" ORDER BY {self._order_by_condition}" if self._order_by_condition else ""
        )
        limit_clause = " LIMIT %s" if self._limit else ""

        query = (
            f"SELECT * FROM {full_table_name(self._table)}"
            + where_clause
            + order_by_clause
            + limit_clause
        )

        return QueryWithParams(
            query,
            self._where_params + self._order_by_params + self._limit_params,
        )

    @override
    def execute(
        self, cursor: Cursor
    ) -> "SelectCursor[GenericTable, GenericColumnAccessor, GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]":
        query, params = self.build()

        return SelectCursor(execute(cursor, query, params), self._table)


class SelectFromWhereOrderByQueryBuilder(
    SelectFinalQueryBuilder[
        GenericTable,
        GenericColumnAccessor,
        GenericInsertColumnTypedDict,
        GenericUpdateColumnTypedDict,
    ]
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
        where_condition: str | None = None,
        where_params: Sequence[Any] | None = None,
        order_by_condition: str | None = None,
        order_by_params: Sequence[Any] | None = None,
    ):
        super().__init__(
            table,
            where_condition=where_condition,
            where_params=where_params,
            order_by_condition=order_by_condition,
            order_by_params=order_by_params,
        )

    def limit(
        self, limit: int
    ) -> "SelectFinalQueryBuilder[GenericTable, GenericColumnAccessor, GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]":
        return SelectFinalQueryBuilder(
            self._table,
            where_condition=self._where_condition,
            where_params=self._where_params,
            order_by_condition=self._order_by_condition,
            order_by_params=self._order_by_params,
            limit=limit,
        )


class SelectFromWhereOrderQueryBuilder(
    Generic[
        GenericTable,
        GenericColumnAccessor,
        GenericInsertColumnTypedDict,
        GenericUpdateColumnTypedDict,
    ]
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
        where_condition: str | None = None,
        where_params: Sequence[Any] | None = None,
    ):
        self._table = table
        self._where_condition = where_condition
        self._where_params = tuple(where_params) if where_params else ()

    @overload
    def by(
        self,
        condition: Callable[
            [
                OrderByContext[
                    GenericTable,
                    GenericColumnAccessor,
                    GenericInsertColumnTypedDict,
                    GenericUpdateColumnTypedDict,
                ]
            ],
            Sequence[Column[Any]] | Column[Any],
        ],
        /,
    ) -> "SelectFromWhereOrderByQueryBuilder[GenericTable, GenericColumnAccessor, GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]": ...

    @overload
    def by(
        self,
        condition: Sequence[Column[Any]] | Column[Any],
        /,
    ) -> "SelectFromWhereOrderByQueryBuilder[GenericTable, GenericColumnAccessor, GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]": ...

    @overload
    def by(
        self,
        condition: str,
        params: Sequence[Any] | None = None,
        /,
    ) -> "SelectFromWhereOrderByQueryBuilder[GenericTable, GenericColumnAccessor, GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]": ...

    def by(
        self,
        condition: Callable[
            [
                OrderByContext[
                    GenericTable,
                    GenericColumnAccessor,
                    GenericInsertColumnTypedDict,
                    GenericUpdateColumnTypedDict,
                ]
            ],
            Sequence[Column[Any]] | Column[Any],
        ]
        | Sequence[Column[Any]]
        | Column[Any]
        | str,
        params: Sequence[Any] | None = None,
        /,
    ) -> "SelectFromWhereOrderByQueryBuilder[GenericTable, GenericColumnAccessor, GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]":
        if callable(condition):
            condition = condition(OrderByContext(self._table))

        if not isinstance(condition, str):
            if isinstance(condition, Column):
                condition = str(condition)
            else:
                condition = ", ".join(str(key) for key in condition)

        return SelectFromWhereOrderByQueryBuilder(
            self._table,
            where_condition=self._where_condition,
            where_params=self._where_params,
            order_by_condition=condition,
            order_by_params=params or (),
        )


class SelectFromWhereQueryBuilder(
    SelectFromWhereOrderByQueryBuilder[
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
        where_condition: str | None = None,
        where_params: Sequence[Any] | None = None,
    ):
        super().__init__(
            table,
            where_condition=where_condition,
            where_params=where_params,
        )

    @property
    def order(
        self,
    ) -> "SelectFromWhereOrderQueryBuilder[GenericTable, GenericColumnAccessor, GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]":
        return SelectFromWhereOrderQueryBuilder(
            self._table,
            where_condition=self._where_condition,
            where_params=self._where_params,
        )


class SelectFromQueryBuilder(
    SelectFromWhereQueryBuilder[
        GenericTable,
        GenericColumnAccessor,
        GenericInsertColumnTypedDict,
        GenericUpdateColumnTypedDict,
    ]
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
        super().__init__(table)

    @overload
    def where(
        self,
        condition: Callable[[WhereContext[GenericColumnAccessor]], Condition],
        /,
    ) -> "SelectFromWhereQueryBuilder[GenericTable, GenericColumnAccessor, GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]": ...

    @overload
    def where(
        self,
        condition: Condition,
        /,
    ) -> "SelectFromWhereQueryBuilder[GenericTable, GenericColumnAccessor, GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]": ...

    @overload
    def where(
        self,
        condition: str,
        params: Sequence[Any] | None = None,
        /,
    ) -> "SelectFromWhereQueryBuilder[GenericTable, GenericColumnAccessor, GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]": ...

    def where(
        self,
        condition: Callable[[WhereContext[GenericColumnAccessor]], Condition]
        | Condition
        | str,
        params: Sequence[Any] | None = None,
        /,
    ) -> "SelectFromWhereQueryBuilder[GenericTable, GenericColumnAccessor, GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]":
        if callable(condition):
            condition, params = condition(WhereContext(self._table)).to_sql()
        elif isinstance(condition, Condition):
            condition, params = condition.to_sql()

        return SelectFromWhereQueryBuilder(
            self._table,
            where_condition=condition,
            where_params=params or (),
        )


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
        self._table = table

    @property
    def rowcount(self) -> int | None:
        return self._cursor.rowcount

    def fetchall(self) -> list[GenericTable]:
        return [
            cast(GenericTable, _map_row(self._table, row))
            for row in self._cursor.fetchall()
        ]

    def fetchmany(self, size: int | None = None) -> list[GenericTable]:
        return [
            cast(GenericTable, _map_row(self._table, row))
            for row in self._cursor.fetchmany(size)
        ]

    def fetchone(self) -> GenericTable | None:
        row = self._cursor.fetchone()

        if row is None:
            return None

        return cast(
            GenericTable,
            _map_row(self._table, row),
        )

    def __iter__(self):
        return self

    def __next__(self) -> GenericTable:
        row = self._cursor.fetchone()

        if row is None:
            raise StopIteration

        return cast(
            GenericTable,
            _map_row(self._table, row),
        )


def _map_row(row_type: Type[GenericTable], row: Any) -> GenericTable:
    return cast(
        GenericTable,
        row_type.model_validate(
            {key: data for key, data in zip(row_type.model_fields.keys(), row)}
        ),
    )
