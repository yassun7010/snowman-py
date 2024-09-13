from typing import Generic, Type

from snowman.query.expression import order
from snowman.relation.table import (
    GenericColumnAccessor,
    GenericInsertColumnTypedDict,
    GenericOrderItemAccessor,
    GenericUpdateColumnTypedDict,
    Table,
)
from snowman.relation.table_like import GenericTableLike
from snowman.relation.view import View


class OrderByContext(
    Generic[
        GenericTableLike,
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
                GenericTableLike,
                GenericColumnAccessor,
                GenericOrderItemAccessor,
                GenericInsertColumnTypedDict,
                GenericUpdateColumnTypedDict,
            ]
            | View[
                GenericColumnAccessor,
                GenericOrderItemAccessor,
            ]
        ],
    ) -> None:
        self._table = table

    def __call__(
        self,
        table: Type[
            Table[
                GenericTableLike,
                GenericColumnAccessor,
                GenericOrderItemAccessor,
                GenericInsertColumnTypedDict,
                GenericUpdateColumnTypedDict,
            ]
            | View[
                GenericColumnAccessor,
                GenericOrderItemAccessor,
            ]
        ],
    ) -> GenericOrderItemAccessor:
        return order(table)

    @property
    def self(self) -> GenericOrderItemAccessor:
        return order(self._table)
