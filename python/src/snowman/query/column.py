from typing import TYPE_CHECKING, Annotated, Any, Generic, Self, Type

from typing_extensions import overload

from snowman._generic import PyType
from snowman.query.condition.is_condition import IsCondition
from snowman.query.condition.is_not_condition import IsNotCondition
from snowman.query.condition.to_condition import ToCondition

if TYPE_CHECKING:

    class _Column(ToCondition[PyType]):
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

    def __str__(self) -> str:
        return ".".join(
            (
                name
                for name in (
                    self._database_name,
                    self._schema_name,
                    self._table_name,
                    self._column_name,
                )
                if name is not None
            )
        )


class ColumnIs(Generic[PyType]):
    def __init__(self, column: Column[PyType]):
        self._column = column

    @property
    def not_(self) -> "ColumnIsNot[PyType]":
        return ColumnIsNot(self._column)

    @property
    def null(self) -> "IsCondition[PyType]":
        return IsCondition(self._column, None)

    @property
    def true(self) -> "IsCondition[PyType]":
        return IsCondition(self._column, True)

    @property
    def false(self) -> "IsCondition[PyType]":
        return IsCondition(self._column, False)


class ColumnIsNot(Generic[PyType]):
    def __init__(self, column: Column[PyType]):
        self._column = column

    @property
    def null(self) -> "IsNotCondition[PyType]":
        return IsNotCondition(self._column, None)

    @property
    def true(self) -> "IsNotCondition[PyType]":
        return IsNotCondition(self._column, True)

    @property
    def false(self) -> "IsNotCondition[PyType]":
        return IsNotCondition(self._column, False)
