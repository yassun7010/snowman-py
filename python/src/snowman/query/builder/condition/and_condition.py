from typing_extensions import override

from snowman.query.builder.condition.condition import Condition
from snowman.query.to_sql import OperationWithParams


class AndCondition(Condition):
    def __init__(self, left: Condition, right: Condition):
        self._left = left
        self._right = right

    @override
    def to_sql(self) -> OperationWithParams:
        left = self._left.to_sql()
        right = self._right.to_sql()
        return OperationWithParams(
            operation=f"{left.operation} AND {right.operation}",
            params=left.params + right.params,
        )
