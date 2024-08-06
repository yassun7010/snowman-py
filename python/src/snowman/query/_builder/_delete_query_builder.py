from typing import TYPE_CHECKING, Any, Callable, Generic, Sequence, Type, overload

from typing_extensions import override

from snowman._features import DeleteTag
from snowman.cursor import Cursor
from snowman.query.condition.to_condition import ToCondition
from snowman.relation import full_table_name
from snowman.relation.table import GenericTable

from ._builder import QueryBuilder, QueryWithParams, execute_with_tag

if TYPE_CHECKING:
    from snowman.context.where_context import WhereContext


class DeleteQueryBuilder:
    def from_(
        self, table: Type[GenericTable], /
    ) -> "DeleteFromStatement[GenericTable]":
        return DeleteFromStatement(table)


class DeleteFromStatement(Generic[GenericTable]):
    def __init__(self, table: Type[GenericTable]):
        self._table = table

    @overload
    def where(
        self,
        condition: Callable[["WhereContext"], ToCondition],
        /,
    ) -> "UpdateFromWhereQueryBuilder[GenericTable]": ...

    @overload
    def where(
        self,
        condition: str,
        params: Sequence[Any] | None = None,
        /,
    ) -> "UpdateFromWhereQueryBuilder[GenericTable]": ...

    def where(
        self,
        condition: str | Callable[["WhereContext"], ToCondition],
        params: Sequence[Any] | None = None,
        /,
    ) -> "UpdateFromWhereQueryBuilder[GenericTable]":
        """
        Specify the condition of the where clause.

        Query parameters only support positional placeholders, so specify them with `%s`.

        e.g)
            `.where("id = %s AND name = %s", [1, "Alice"])`
        """
        if callable(condition):
            from snowman.context.where_context import WhereContext

            condition, params = condition(WhereContext()).to_condition()

        return UpdateFromWhereQueryBuilder(self._table, condition, params or ())


class UpdateFromWhereQueryBuilder(Generic[GenericTable], QueryBuilder):
    def __init__(
        self,
        table: Type[GenericTable],
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
