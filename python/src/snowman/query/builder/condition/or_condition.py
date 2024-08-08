from typing_extensions import override

from snowman.query.builder.condition.condition import Condition, ConditionWithParams


class OrCondition(Condition):
    def __init__(self, left: Condition, right: Condition):
        self._left = left
        self._right = right

    @override
    def to_sql(self) -> ConditionWithParams:
        left = self._left.to_sql()
        right = self._right.to_sql()
        return ConditionWithParams(
            f"{left.condition} OR {right.condition}",
            left.params + right.params,
        )
