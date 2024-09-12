from typing_extensions import override

from snowman.query.builder.condition.condition import Condition
from snowman.query.to_sql import OperationWithParams


class OrCondition(Condition):
    def __init__(self, left: Condition, right: Condition):
        self._left = left
        self._right = right

    @override
    def to_sql(self) -> OperationWithParams:
        left = self._left.to_sql()
        right = self._right.to_sql()
        return OperationWithParams(
            f"{left.operation} OR {right.operation}",
            left.params + right.params,
        )
