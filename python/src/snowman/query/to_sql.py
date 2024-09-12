from abc import ABC, abstractmethod
from typing import Any, NamedTuple


class OperationWithParams(NamedTuple):
    operation: str
    params: tuple[Any, ...]


class ToSql(ABC):
    @abstractmethod
    def to_sql(self) -> OperationWithParams: ...
