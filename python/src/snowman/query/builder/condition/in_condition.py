from typing import TYPE_CHECKING, Sequence

from snowman._generic import PyType
from snowman.query.builder.condition.condition import Condition, ConditionWithParams

if TYPE_CHECKING:
    from snowman.query.column import Column


class InCondition(Condition):
    def __init__(self, base: "Column[PyType]", values: Sequence[PyType]):
        self._base = base
        self._values = values

    def to_sql(self) -> ConditionWithParams:
        return ConditionWithParams(
            condition=f"{self._base} IN (%s)", params=(self._values,)
        )
