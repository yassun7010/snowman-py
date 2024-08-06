from typing import overload

from snowman._generic import PyType
from snowman.query.column import Column
from snowman.query.condition.and_condition import AndCondition
from snowman.query.condition.or_condition import OrCondition
from snowman.query.condition.to_condition import ToCondition


class WhereContext:
    @overload
    def __call__(self, column: Column[PyType]) -> Column[PyType]: ...

    @overload
    def __call__(self, column: PyType) -> Column[PyType]: ...

    def __call__(self, column: Column[PyType] | PyType) -> Column[PyType]:
        return column  # type: ignore

    def and_(self, left: ToCondition, right: ToCondition) -> AndCondition:
        return AndCondition(left, right)

    def or_(self, left: ToCondition, right: ToCondition) -> OrCondition:
        return OrCondition(left, right)
