from typing import Generic, Type

from snowman.query.builder.condition.condition import Condition
from snowman.query.builder.condition.group_condition import GroupCondition
from snowman.query.column import column
from snowman.relation.table import (
    GenericColumnAccessor,
    GenericInsertColumnTypedDict,
    GenericUpdateColumnTypedDict,
    Table,
)


class WhereContext(Generic[GenericColumnAccessor]):
    def __call__(
        self,
        table: Type[
            Table[
                GenericColumnAccessor,
                GenericInsertColumnTypedDict,
                GenericUpdateColumnTypedDict,
            ]
        ],
    ) -> GenericColumnAccessor:
        return column(table)

    def group(self, condition: Condition, /) -> GroupCondition:
        return group(condition)


def group(condition: Condition) -> GroupCondition:
    return GroupCondition(condition)
