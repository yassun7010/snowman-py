from typing import Any, Generic, Type, cast

from pydantic.fields import FieldInfo
from typing_extensions import override

from snowman._generic import PyType
from snowman.query.column import Column, GenericColumnName
from snowman.query.to_sql import OperationWithParams, ToSql
from snowman.relation.table import (
    GenericColumnAccessor,
    GenericInsertColumnTypedDict,
    GenericOrderItemAccessor,
    GenericTable,
    GenericUpdateColumnTypedDict,
    Table,
)
from snowman.relation.view import View


class OrderItem(Generic[GenericTable, GenericColumnName, PyType], ToSql):
    pass


class ColumnOrderItem(
    OrderItem[GenericTable, GenericColumnName, PyType],
):
    def __init__(self, column: Column[GenericTable, GenericColumnName, PyType]):
        self._column = column

    @property
    def asc(self) -> "AscOrderItem[GenericTable, GenericColumnName, PyType]":
        return AscOrderItem(self)

    @property
    def desc(self) -> "DescOrderItem[GenericTable, GenericColumnName, PyType]":
        return DescOrderItem(self)

    @property
    def nulls(self) -> "NullsOrderItem[GenericTable, GenericColumnName, PyType]":
        return NullsOrderItem(self)

    @override
    def to_sql(self) -> OperationWithParams:
        return OperationWithParams(
            operation=str(self._column),
            params=(),
        )

    def __str__(self) -> str:
        return str(self._column)

    def __repr__(self) -> str:
        return repr(self._column)


class AscOrderItem(OrderItem[GenericTable, GenericColumnName, PyType]):
    def __init__(self, order_item: OrderItem[GenericTable, GenericColumnName, PyType]):
        self._order_item = order_item

    @property
    def nulls(self) -> "NullsOrderItem[GenericTable, GenericColumnName, PyType]":
        return NullsOrderItem(self)

    @override
    def to_sql(self) -> OperationWithParams:
        operation, params = self._order_item.to_sql()
        return OperationWithParams(
            operation=f"{operation} ASC",
            params=params,
        )


class DescOrderItem(OrderItem[GenericTable, GenericColumnName, PyType]):
    def __init__(self, order_item: OrderItem[GenericTable, GenericColumnName, PyType]):
        self._order_item = order_item

    @property
    def nulls(self) -> "NullsOrderItem[GenericTable, GenericColumnName, PyType]":
        return NullsOrderItem(self)

    @override
    def to_sql(self) -> OperationWithParams:
        operation, params = self._order_item.to_sql()
        return OperationWithParams(
            operation=f"{operation} DESC",
            params=params,
        )


class NullsOrderItem(Generic[GenericTable, GenericColumnName, PyType]):
    def __init__(self, item: OrderItem):
        self._item = item

    @property
    def first(self) -> "NullsFirstOrderItem[GenericTable, GenericColumnName, PyType]":
        return NullsFirstOrderItem(self._item)

    @property
    def last(self) -> "NullsLastOrderItem[GenericTable, GenericColumnName, PyType]":
        return NullsLastOrderItem(self._item)


class NullsFirstOrderItem(OrderItem[GenericTable, GenericColumnName, PyType]):
    def __init__(self, item: OrderItem):
        self._item = item

    @override
    def to_sql(self) -> OperationWithParams:
        operation, params = self._item.to_sql()
        return OperationWithParams(
            operation=f"{operation} NULLS FIRST",
            params=params,
        )


class NullsLastOrderItem(OrderItem[GenericTable, GenericColumnName, PyType]):
    def __init__(self, item: OrderItem):
        self._item = item

    @override
    def to_sql(self) -> OperationWithParams:
        operation, params = self._item.to_sql()

        return OperationWithParams(
            operation=f"{operation} NULLS LAST",
            params=params,
        )


class _InternalOrderItemAccessor:
    """
    An internal implementation class for accessing column information.

    On the editor, this class behaves as GenericColumnAccessor,
    but this class is called when accessing properties.
    """

    def __init__(
        self,
        table: Type[
            Table[
                GenericTable,
                GenericColumnAccessor,
                GenericOrderItemAccessor,
                GenericInsertColumnTypedDict,
                GenericUpdateColumnTypedDict,
            ]
            | View[GenericColumnAccessor, GenericOrderItemAccessor]
        ],
    ):
        self._table = table

    def __getattr__(self, key: str) -> OrderItem[Any, Any, Any]:
        field: FieldInfo = self._table.model_fields[key]
        return ColumnOrderItem(
            Column(
                cast(type, field.annotation),
                database_name=self._table.__database_name__,
                schema_name=self._table.__schema_name__,
                table_name=self._table.__table_name__,
                column_name=field.alias if field.alias else key,
            )
        )
