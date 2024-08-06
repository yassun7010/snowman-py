from abc import ABC, abstractmethod
from typing import Any, NamedTuple


class ConditionWithParams(NamedTuple):
    condition: str
    params: tuple[Any, ...]


class ToCondition(ABC):
    @abstractmethod
    def to_condition(self) -> ConditionWithParams: ...
