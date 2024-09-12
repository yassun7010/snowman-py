from typing import TYPE_CHECKING, Sequence

from snowman._generic import PyType
from snowman.query.builder.condition.condition import Condition
from snowman.query.to_sql import OperationWithParams

if TYPE_CHECKING:
    from snowman.query.column import Column


class NotInCondition(Condition):
    def __init__(self, base: "Column[PyType]", values: Sequence[PyType]):
        self._base = base
        self._values = values

    def to_sql(self) -> OperationWithParams:
        return OperationWithParams(
            operation=f"{self._base} NOT IN (%s)", params=(self._values,)
        )
