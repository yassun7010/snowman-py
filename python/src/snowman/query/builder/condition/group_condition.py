from typing import TYPE_CHECKING

from snowman.query.builder.condition.condition import Condition
from snowman.query.to_sql import OperationWithParams

if TYPE_CHECKING:
    pass


class GroupCondition(Condition):
    def __init__(self, condition: Condition, /):
        self._condition = condition

    def to_sql(self) -> OperationWithParams:
        sql = self._condition.to_sql()
        return OperationWithParams(operation=f"({sql.operation})", params=sql.params)
