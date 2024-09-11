from typing import Generic, Type

from snowman.query.builder.condition.condition import Condition
from snowman.query.builder.condition.group_condition import GroupCondition
from snowman.query.expression import column, group
from snowman.relation.table import (
    GenericColumnAccessor,
    GenericInsertColumnTypedDict,
    GenericTable,
    GenericUpdateColumnTypedDict,
    Table,
)


class WhereContext(Generic[GenericColumnAccessor]):
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

    def group(self, condition: Condition, /) -> GroupCondition:
        return group(condition)

    @property
    def self(self) -> GenericColumnAccessor:
        return column(self._table)
