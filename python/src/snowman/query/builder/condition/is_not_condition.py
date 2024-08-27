from typing import TYPE_CHECKING

from typing_extensions import override

from snowman._generic import PyType
from snowman.query.builder.condition.condition import Condition, ConditionWithParams

if TYPE_CHECKING:
    from snowman.query.column import Column


class IsNotCondition(Condition):
    def __init__(self, base: "Column[PyType]"):
        self._base = base

    @override
    def to_sql(self) -> ConditionWithParams:
        return ConditionWithParams(condition=f"{self._base} IS NOT NULL", params=())
