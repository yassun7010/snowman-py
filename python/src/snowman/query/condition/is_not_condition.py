from typing import TYPE_CHECKING

from typing_extensions import override

from snowman._generic import PyType
from snowman.query.condition.to_condition import ConditionWithParams, ToCondition

if TYPE_CHECKING:
    from snowman.query.column import Column


class IsNotCondition(ToCondition[PyType]):
    def __init__(self, base: "Column[PyType]", value: bool | None):
        self._base = base
        self._value = value

    @override
    def to_condition(self) -> ConditionWithParams:
        value = "NULL" if self._value is None else str(self._value).upper()
        return ConditionWithParams(condition=f"{self._base} IS NOT {value}", params=())
