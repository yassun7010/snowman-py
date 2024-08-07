from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, NamedTuple

if TYPE_CHECKING:
    from snowman.query.condition.and_condition import AndCondition
    from snowman.query.condition.or_condition import OrCondition


class ConditionWithParams(NamedTuple):
    condition: str
    params: tuple[Any, ...]


class ToCondition(ABC):
    @abstractmethod
    def to_condition(self) -> ConditionWithParams: ...

    def and_(self, other: "ToCondition") -> "AndCondition":
        from snowman.query.condition.and_condition import AndCondition

        return AndCondition(self, other)

    def or_(self, other: "ToCondition") -> "OrCondition":
        from snowman.query.condition.or_condition import OrCondition

        return OrCondition(self, other)
