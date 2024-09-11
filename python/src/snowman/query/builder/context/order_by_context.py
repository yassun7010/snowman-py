from typing import Generic, Type

from snowman.query.expression import column
from snowman.relation.table import (
    GenericColumnAccessor,
    GenericInsertColumnTypedDict,
    GenericTable,
    GenericUpdateColumnTypedDict,
    Table,
)


class OrderByContext(
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
    ) -> None:
        self._table = table

    def __call__(
        self,
        table: Type[
            Table[
                GenericTable,
                GenericColumnAccessor,
                GenericInsertColumnTypedDict,
                GenericUpdateColumnTypedDict,
            ]
        ],
    ) -> GenericColumnAccessor:
        return column(table)

    @property
    def self(self) -> GenericColumnAccessor:
        return column(self._table)
