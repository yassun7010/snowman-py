from typing_extensions import override

from snowman.query.condition.to_condition import ConditionWithParams, ToCondition


class AndCondition(ToCondition):
    def __init__(self, left: ToCondition, right: ToCondition):
        self._left = left
        self._right = right

    @override
    def to_condition(self) -> ConditionWithParams:
        left = self._left.to_condition()
        right = self._right.to_condition()
        return ConditionWithParams(
            f"{left.condition} AND {right.condition}",
            left.params + right.params,
        )
