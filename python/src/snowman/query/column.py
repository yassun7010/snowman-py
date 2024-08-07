from typing import TYPE_CHECKING, Any, Generic, Type, cast, overload

from snowman._generic import PyType
from snowman.query.condition.eq_condition import EqCondition
from snowman.query.condition.is_condition import IsCondition
from snowman.query.condition.is_not_condition import IsNotCondition
from snowman.query.condition.ne_condition import NeCondition
from snowman.relation.table import (
    GenericColumnAccessor,
    GenericInsertColumnTypedDict,
    GenericUpdateColumnTypedDict,
    Table,
)

if TYPE_CHECKING:
    from snowman.typing import TypeMissMatch, U


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

    @overload
    def __eq__(self, value: PyType) -> EqCondition: ...  # type: ignore
    @overload
    def __eq__(self, value: "U") -> "TypeMissMatch[PyType, U]": ...
    def __eq__(self, value: PyType) -> EqCondition:  # type: ignore
        return EqCondition(self, value)

    @overload
    def __ne__(self, value: PyType) -> EqCondition: ...  # type: ignore
    @overload
    def __ne__(self, value: "U") -> "TypeMissMatch[PyType, U]": ...
    def __ne__(self, value: PyType) -> NeCondition:  # type: ignore
        return NeCondition(self, value)

    def __str__(self) -> str:
        return self._column_name

    def __repr__(self) -> str:
        return f"{self._database_name}.{self._schema_name}.{self._table_name}.{self._column_name}"


class ColumnAccessor:
    def __init__(
        self,
        table: Type[
            Table[
                GenericColumnAccessor,
                GenericInsertColumnTypedDict,
                GenericUpdateColumnTypedDict,
            ]
        ],
    ):
        self._table = table

    def __getattr__(self, key: str) -> Column[Any]:
        return Column(
            cast(type, self._table.model_fields[key].annotation),
            database_name=self._table.__database_name__,
            schema_name=self._table.__schema_name__,
            table_name=self._table.__table_name__,
            column_name=key,
        )


def get_columns(
    table: Type[
        Table[
            GenericColumnAccessor,
            GenericInsertColumnTypedDict,
            GenericUpdateColumnTypedDict,
        ]
    ],
) -> GenericColumnAccessor:
    return cast(GenericColumnAccessor, ColumnAccessor(table))


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
