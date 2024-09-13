from typing import TYPE_CHECKING

from typing_extensions import override

from snowman._generic import PyType
from snowman.query.builder.condition.condition import Condition
from snowman.query.to_sql import OperationWithParams

if TYPE_CHECKING:
    from snowman.query.column import Column, GenericColumnName
    from snowman.relation.table_like import GenericTableLike


class IsNotCondition(Condition):
    def __init__(self, base: "Column[GenericTableLike, GenericColumnName,PyType]"):
        self._base = base

    @override
    def to_sql(self) -> OperationWithParams:
        return OperationWithParams(operation=f"{self._base} IS NOT NULL", params=())
