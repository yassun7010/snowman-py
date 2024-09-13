from typing import Generic, Type

from snowman.query.expression import order
from snowman.relation.table import (
    GenericColumnAccessor,
    GenericInsertColumnTypedDict,
    GenericOrderItemAccessor,
    GenericTable,
    GenericUpdateColumnTypedDict,
    Table,
)


class OrderByContext(
    Generic[
        GenericTable,
        GenericColumnAccessor,
        GenericOrderItemAccessor,
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
                GenericOrderItemAccessor,
                GenericInsertColumnTypedDict,
                GenericUpdateColumnTypedDict,
            ]
        ],
    ) -> None:
        self._table = table

    def __call__(
        self,
        table: Type[
            Table[
                GenericTable,
                GenericColumnAccessor,
                GenericOrderItemAccessor,
                GenericInsertColumnTypedDict,
                GenericUpdateColumnTypedDict,
            ]
        ],
    ) -> GenericOrderItemAccessor:
        return order(table)

    @property
    def self(self) -> GenericOrderItemAccessor:
        return order(self._table)
