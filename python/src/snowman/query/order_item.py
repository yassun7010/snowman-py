from typing_extensions import override

from snowman._generic import PyType
from snowman.query.column import Column
from snowman.query.to_sql import OperationWithParams, ToSql


class OrderItem(ToSql):
    pass


class ColumnOrderItem(Column[PyType], OrderItem):
    def __init__(self, column: Column[PyType]):
        self._column = column

    @property
    def asc(self) -> "AscOrderItem":
        return AscOrderItem(self)

    @property
    def desc(self) -> "DescOrderItem":
        return DescOrderItem(self)

    @property
    def nulls(self) -> "NullsOrderItem":
        return NullsOrderItem(self)

    @override
    def to_sql(self) -> OperationWithParams:
        return OperationWithParams(
            operation=str(self._column),
            params=(),
        )


class AscOrderItem(OrderItem):
    def __init__(self, order_item: OrderItem):
        self._order_item = order_item

    @property
    def nulls(self) -> "NullsOrderItem":
        return NullsOrderItem(self)

    @override
    def to_sql(self) -> OperationWithParams:
        operation, params = self._order_item.to_sql()
        return OperationWithParams(
            operation=f"{operation} ASC",
            params=params,
        )


class DescOrderItem(OrderItem):
    def __init__(self, order_item: OrderItem):
        self._order_item = order_item

    @property
    def nulls(self) -> "NullsOrderItem":
        return NullsOrderItem(self)

    @override
    def to_sql(self) -> OperationWithParams:
        operation, params = self._order_item.to_sql()
        return OperationWithParams(
            operation=f"{operation} DESC",
            params=params,
        )


class NullsOrderItem:
    def __init__(self, item: OrderItem):
        self._item = item

    @property
    def first(self) -> "NullsFirstOrderItem":
        return NullsFirstOrderItem(self._item)

    @property
    def last(self) -> "NullsLastOrderItem":
        return NullsLastOrderItem(self._item)


class NullsFirstOrderItem(OrderItem):
    def __init__(self, item: OrderItem):
        self._item = item

    @override
    def to_sql(self) -> OperationWithParams:
        operation, params = self._item.to_sql()
        return OperationWithParams(
            operation=f"{operation} NULLS FIRST",
            params=params,
        )


class NullsLastOrderItem(NullsOrderItem, OrderItem):
    def __init__(self, item: OrderItem):
        self._item = item

    @override
    def to_sql(self) -> OperationWithParams:
        operation, params = self._item.to_sql()

        return OperationWithParams(
            operation=f"{operation} NULLS LAST",
            params=params,
        )
