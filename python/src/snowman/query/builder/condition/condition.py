from typing import TYPE_CHECKING

from snowman.query.to_sql import ToSql

if TYPE_CHECKING:
    from snowman.query.builder.condition.and_condition import AndCondition
    from snowman.query.builder.condition.or_condition import OrCondition


class Condition(ToSql):
    def and_(self, other: "Condition") -> "AndCondition":
        from snowman.query.builder.condition.and_condition import AndCondition

        return AndCondition(self, other)

    def or_(self, other: "Condition") -> "OrCondition":
        from snowman.query.builder.condition.or_condition import OrCondition

        return OrCondition(self, other)
