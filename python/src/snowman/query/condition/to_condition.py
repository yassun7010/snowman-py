from abc import ABC, abstractmethod
from typing import Any, Generic

from snowman._generic import PyType


class ToCondition(Generic[PyType], ABC):
    @abstractmethod
    def to_condition(self, params: list[Any]) -> str: ...
