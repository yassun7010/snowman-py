from typing import Any, Callable, Generic, Sequence, Type, overload

from typing_extensions import override

from snowman._features import DeleteTag
from snowman.context.where_context import WhereContext
from snowman.cursor import Cursor
from snowman.query.condition.to_condition import ToCondition
from snowman.relation import full_table_name
from snowman.relation.table import (
    GenericColumnAccessor,
    GenericInsertColumnTypedDict,
    GenericUpdateColumnTypedDict,
    Table,
)

from ._builder import QueryBuilder, QueryWithParams, execute_with_tag


class DeleteQueryBuilder:
    def from_(
        self,
        table: Type[
            Table[
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
        condition: Callable[[WhereContext[GenericColumnAccessor]], ToCondition],
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
        condition: str | Callable[[WhereContext[GenericColumnAccessor]], ToCondition],
        params: Sequence[Any] | None = None,
        /,
    ) -> "DeleteFromWhereQueryBuilder":
        """
        Specify the condition of the where clause.

        Query parameters only support positional placeholders, so specify them with `%s`.

        e.g)
            `.where("id = %s AND name = %s", [1, "Alice"])`
        """
        if callable(condition):
            condition, params = condition(WhereContext()).to_condition()

        return DeleteFromWhereQueryBuilder(self._table, condition, params or ())


class DeleteFromWhereQueryBuilder(QueryBuilder):
    def __init__(
        self,
        table: Type[
            Table[
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
DELETE FROM
    {full_table_name(self._table)}
WHERE
    {self._where_condition}
""".strip()

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
