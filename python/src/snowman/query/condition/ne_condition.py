from typing import TYPE_CHECKING

from snowman._generic import PyType
from snowman.query.condition.to_condition import ConditionWithParams, ToCondition

if TYPE_CHECKING:
    from snowman.query.column import Column


class NeCondition(ToCondition):
    def __init__(self, base: "Column[PyType]", value: PyType):
        self._base = base
        self._value = value

    def to_condition(self) -> ConditionWithParams:
        return ConditionWithParams(
            condition=f"{self._base} != %s", params=(self._value,)
        )
