from abc import ABC, abstractmethod
from typing import Any, Generic, NamedTuple

from snowman._generic import PyType


class ConditionWithParams(NamedTuple):
    condition: str
    params: tuple[Any, ...]


class ToCondition(Generic[PyType], ABC):
    @abstractmethod
    def to_condition(self) -> ConditionWithParams: ...
