from typing import TYPE_CHECKING

from snowman._generic import PyType
from snowman.query.builder.condition.condition import Condition
from snowman.query.to_sql import OperationWithParams

if TYPE_CHECKING:
    from snowman.query.column import Column


class GeCondition(Condition):
    def __init__(self, base: "Column[PyType]", value: PyType):
        self._base = base
        self._value = value

    def to_sql(self) -> OperationWithParams:
        return OperationWithParams(
            operation=f"{self._base} >= %s", params=(self._value,)
        )
