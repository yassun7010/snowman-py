from typing import Generic, Type

from snowman.query.builder.condition.condition import Condition
from snowman.query.builder.condition.group_condition import GroupCondition
from snowman.query.expression import column, group
from snowman.relation.table import (
    GenericColumnAccessor,
    GenericInsertColumnTypedDict,
    GenericOrderItemAccessor,
    GenericUpdateColumnTypedDict,
    Table,
)
from snowman.relation.table_like import GenericTableLike
from snowman.relation.view import View


class WhereContext(Generic[GenericColumnAccessor]):
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
        ],
    ) -> GenericColumnAccessor:
        return column(table)

    def group(self, condition: Condition, /) -> GroupCondition:
        return group(condition)

    @property
    def self(self) -> GenericColumnAccessor:
        return column(self._table)
