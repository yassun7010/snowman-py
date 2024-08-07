from typing import Generic, Type

from snowman.query.column import get_columns
from snowman.query.condition.condition import Condition
from snowman.query.condition.group_condition import GroupCondition
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
        return get_columns(table)

    def group(self, condition: Condition, /) -> "GroupCondition":
        return GroupCondition(condition)
