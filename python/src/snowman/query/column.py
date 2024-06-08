from typing import TYPE_CHECKING, Annotated, Any, Generic, Self, Type

from typing_extensions import overload

from snowman._generic import PyType
from snowman.query.condition import IsCondition, IsNotCondition
from snowman.query.condition.to_condition import ToCondition

if TYPE_CHECKING:

    class Column(ToCondition[PyType]):
        @overload
        def __get__(self, instance: None, owner: Type[Any]) -> "Self": ...

        @overload
        def __get__(self, instance: object, owner: Type[Any]) -> PyType: ...

        def __get__(
            self, instance: object | None, owner: Type[Any]
        ) -> "Self | PyType": ...

        @property
        def is_(self) -> "ColumnIs[PyType]": ...

else:
    Column = Annotated[PyType, ...]


class _Column(Generic[PyType]):
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
    def __init__(self, column: _Column[PyType]):
        self._column = column

    def not_(self, value: bool | None) -> "IsNotCondition[PyType]":
        return IsNotCondition(self._column, value)

    def __call__(self, value: bool | None) -> "IsCondition[PyType]":
        return IsCondition(self._column, value)
