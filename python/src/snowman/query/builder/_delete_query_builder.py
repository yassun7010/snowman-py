from typing import Any, Callable, Generic, Sequence, Type, overload

from typing_extensions import override

from snowman._cursor import Cursor
from snowman._features import DeleteTag
from snowman.query.builder.condition.condition import Condition
from snowman.query.builder.context.where_context import WhereContext
from snowman.relation import full_table_name
from snowman.relation.table import (
    GenericColumnAccessor,
    GenericInsertColumnTypedDict,
    GenericTable,
    GenericUpdateColumnTypedDict,
    Table,
)

from ._builder import QueryBuilder, QueryWithParams, execute_with_tag


class DeleteQueryBuilder:
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
    ) -> "DeleteFromStatement[GenericColumnAccessor]":
        return DeleteFromStatement(table)


class DeleteFromStatement(Generic[GenericColumnAccessor]):
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
    ) -> "DeleteFromWhereQueryBuilder": ...

    @overload
    def where(
        self,
        condition: Condition,
        /,
    ) -> "DeleteFromWhereQueryBuilder": ...

    @overload
    def where(
        self,
        condition: str,
        params: Sequence[Any] | None = None,
        /,
    ) -> "DeleteFromWhereQueryBuilder": ...

    def where(
        self,
        condition: Callable[[WhereContext[GenericColumnAccessor]], Condition]
        | Condition
        | str,
        params: Sequence[Any] | None = None,
        /,
    ) -> "DeleteFromWhereQueryBuilder":
        """
        Specify the condition of the where clause.

        Query parameters only support positional placeholders, so specify them with `%s`.

        e.g)
            - `.where(lambda c: (c(User).id == 1).and_(c(User).name == "Alice"))`
            - `.where((column(User).id == 1).and_(column(User).name == "Alice"))`
            - `.where("id = %s AND name = %s", [1, "Alice"])`
        """
        if callable(condition):
            condition, params = condition(WhereContext(self._table)).to_sql()

        elif isinstance(condition, Condition):
            condition, params = condition.to_sql()

        return DeleteFromWhereQueryBuilder(self._table, condition, params or ())


class DeleteFromWhereQueryBuilder(QueryBuilder[None]):
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
        query = f"DELETE FROM {full_table_name(self._table)} WHERE {self._where_condition}".strip()

        return QueryWithParams(query, tuple(self._where_params))

    @override
    def execute(self, cursor: Cursor) -> None:
        query, params = self.build()

        execute_with_tag(
            DeleteTag[self._table],  # type: ignore
            cursor,
            query,
            params,
        )
