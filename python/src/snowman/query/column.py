from typing import TYPE_CHECKING, Annotated, Any, Generic, Self, Type

from typing_extensions import overload

from snowman._generic import PyType
from snowman.query.condition.eq_condition import EqCondition
from snowman.query.condition.is_condition import IsCondition
from snowman.query.condition.is_not_condition import IsNotCondition

if TYPE_CHECKING:

    class _Column(Generic[PyType]):
        @overload
        def __get__(self, instance: None, owner: Type[Any]) -> "Self": ...

        @overload
        def __get__(self, instance: object, owner: Type[Any]) -> PyType: ...

        def __get__(
            self, instance: object | None, owner: Type[Any]
        ) -> "Self | PyType": ...

else:
    _Column = Annotated[PyType, ...]


class Column(Generic[PyType]):
    def __init__(
        self,
        data_type: Type[PyType],
        /,
        *,
        database_name: str,
        schema_name: str,
        table_name: str,
        column_name: str,
    ):
        self._data_type = data_type
        self._database_name = database_name
        self._schema_name = schema_name
        self._table_name = table_name
        self._column_name = column_name

    @property
    def is_(self) -> "ColumnIs[PyType]":
        return ColumnIs(self)

    def __eq__(self, value: PyType) -> EqCondition:
        return EqCondition(self, value)

    def __str__(self) -> str:
        return self._column_name

    def __repr__(self) -> str:
        return f"{self._database_name}.{self._schema_name}.{self._table_name}.{self._column_name}"


class ColumnIs(Generic[PyType]):
    def __init__(self, column: Column[PyType]):
        self._column = column

    @property
    def not_(self) -> "ColumnIsNot":
        return ColumnIsNot(self._column)

    @property
    def null(self) -> "IsCondition":
        return IsCondition(self._column, None)

    @property
    def true(self) -> "IsCondition":
        return IsCondition(self._column, True)

    @property
    def false(self) -> "IsCondition":
        return IsCondition(self._column, False)


class ColumnIsNot(Generic[PyType]):
    def __init__(self, column: Column[PyType]):
        self._column = column

    @property
    def null(self) -> "IsNotCondition":
        return IsNotCondition(self._column, None)

    @property
    def true(self) -> "IsNotCondition":
        return IsNotCondition(self._column, True)

    @property
    def false(self) -> "IsNotCondition":
        return IsNotCondition(self._column, False)
