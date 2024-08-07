from typing import TYPE_CHECKING

from snowman.query.builder.condition.condition import Condition, ConditionWithParams

if TYPE_CHECKING:
    pass


class GroupCondition(Condition):
    def __init__(self, condition: Condition, /):
        self._condition = condition

    def to_sql(self) -> ConditionWithParams:
        sql = self._condition.to_sql()
        return ConditionWithParams(condition=f"({sql.condition})", params=sql.params)
