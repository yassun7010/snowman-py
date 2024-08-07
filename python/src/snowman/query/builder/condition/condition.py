from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, NamedTuple

if TYPE_CHECKING:
    from snowman.query.builder.condition.and_condition import AndCondition
    from snowman.query.builder.condition.or_condition import OrCondition


class ConditionWithParams(NamedTuple):
    condition: str
    params: tuple[Any, ...]


class Condition(ABC):
    @abstractmethod
    def to_sql(self) -> ConditionWithParams: ...

    def and_(self, other: "Condition") -> "AndCondition":
        from snowman.query.builder.condition.and_condition import AndCondition

        return AndCondition(self, other)

    def or_(self, other: "Condition") -> "OrCondition":
        from snowman.query.builder.condition.or_condition import OrCondition

        return OrCondition(self, other)
