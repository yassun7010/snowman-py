from typing import TYPE_CHECKING, Any, Generic

from typing_extensions import override

from snowman._generic import PyType
from snowman.query.condition.to_condition import ToCondition

if TYPE_CHECKING:
    from snowman.query.column import _Column


class Condition(Generic[PyType]):
    pass


class IsCondition(ToCondition[PyType]):
    def __init__(self, base: "_Column[PyType]", value: bool | None):
        self._base = base
        self._value = value

    @override
    def to_condition(self, params: list[Any]) -> str:
        value = "NULL" if self._value is None else str(self._value).upper()
        return f"{self._base} IS {value}"


class IsNotCondition(ToCondition[PyType]):
    def __init__(self, base: "_Column[PyType]", value: bool | None):
        self._base = base
        self._value = value

    @override
    def to_condition(self, params: list[Any]) -> str:
        value = "NULL" if self._value is None else str(self._value).upper()
        return f"{self._base} IS NOT {value}"
