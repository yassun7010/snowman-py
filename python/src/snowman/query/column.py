from typing import TYPE_CHECKING, Any, Generic, Sequence, Type, cast, overload

from pydantic.fields import FieldInfo

from snowman._generic import PyType
from snowman.query.builder.condition.eq_condition import EqCondition
from snowman.query.builder.condition.ge_condition import GeCondition
from snowman.query.builder.condition.gt_condition import GtCondition
from snowman.query.builder.condition.in_condition import InCondition
from snowman.query.builder.condition.is_condition import IsCondition
from snowman.query.builder.condition.is_not_condition import IsNotCondition
from snowman.query.builder.condition.le_condition import LeCondition
from snowman.query.builder.condition.lt_condition import LtCondition
from snowman.query.builder.condition.ne_condition import NeCondition
from snowman.query.builder.condition.not_in_condition import NotInCondition
from snowman.relation.table import (
    GenericColumnAccessor,
    GenericInsertColumnTypedDict,
    GenericTable,
    GenericUpdateColumnTypedDict,
    Table,
)
from snowman.relation.view import View

if TYPE_CHECKING:
    from snowman.typing import (
        TypeMissMatch,
        U,
        UseIsInsteadOfEq,
        UseIsNotInsteadOfNe,
    )


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

    def in_(self, values: Sequence[PyType], /) -> InCondition:
        return InCondition(self, values)

    @property
    def not_(self) -> "ColumnNot[PyType]":
        return ColumnNot(self)

    @overload
    def __eq__(self, value: bool) -> "UseIsInsteadOfEq": ...  # type: ignore
    @overload
    def __eq__(self, value: None) -> "UseIsInsteadOfEq": ...  # type: ignore
    @overload
    def __eq__(self, value: PyType) -> EqCondition: ...  # type: ignore
    @overload
    def __eq__(self, value: "U") -> "TypeMissMatch[PyType, U]": ...
    def __eq__(self, value: PyType) -> EqCondition:  # type: ignore
        return EqCondition(self, value)

    @overload
    def __ne__(self, value: bool) -> "UseIsNotInsteadOfNe": ...  # type: ignore
    @overload
    def __ne__(self, value: None) -> "UseIsNotInsteadOfNe": ...  # type: ignore
    @overload
    def __ne__(self, value: PyType) -> NeCondition: ...  # type: ignore
    @overload
    def __ne__(self, value: "U") -> "TypeMissMatch[PyType, U]": ...
    def __ne__(self, value: PyType) -> NeCondition:  # type: ignore
        return NeCondition(self, value)

    @overload
    def __le__(self, value: PyType) -> LeCondition: ...  # type: ignore
    @overload
    def __le__(self, value: "U") -> "TypeMissMatch[PyType, U]": ...
    def __le__(self, value: PyType) -> LeCondition:  # type: ignore
        return LeCondition(self, value)

    @overload
    def __ge__(self, value: PyType) -> GeCondition: ...  # type: ignore
    @overload
    def __ge__(self, value: "U") -> "TypeMissMatch[PyType, U]": ...
    def __ge__(self, value: PyType) -> GeCondition:  # type: ignore
        return GeCondition(self, value)

    @overload
    def __lt__(self, value: PyType) -> LtCondition: ...  # type: ignore
    @overload
    def __lt__(self, value: "U") -> "TypeMissMatch[PyType, U]": ...
    def __lt__(self, value: PyType) -> LtCondition:  # type: ignore
        return LtCondition(self, value)

    @overload
    def __gt__(self, value: PyType) -> GtCondition: ...  # type: ignore
    @overload
    def __gt__(self, value: "U") -> "TypeMissMatch[PyType, U]": ...
    def __gt__(self, value: PyType) -> GtCondition:  # type: ignore
        return GtCondition(self, value)

    def __str__(self) -> str:
        return self._column_name

    def __repr__(self) -> str:
        return f"{self._database_name}.{self._schema_name}.{self._table_name}.{self._column_name}"


class _InternalColumnAccessor:
    """
    An internal implementation class for accessing column information.

    On the editor, this class behaves as GenericColumnAccessor,
    but this class is called when accessing properties.
    """

    def __init__(
        self,
        table: Type[
            Table[
                GenericTable,
                GenericColumnAccessor,
                GenericInsertColumnTypedDict,
                GenericUpdateColumnTypedDict,
            ]
            | View[GenericColumnAccessor]
        ],
    ):
        self._table = table

    def __getattr__(self, key: str) -> Column[Any]:
        field: FieldInfo = self._table.model_fields[key]
        return Column(
            cast(type, field.annotation),
            database_name=self._table.__database_name__,
            schema_name=self._table.__schema_name__,
            table_name=self._table.__table_name__,
            column_name=field.alias if field.alias else key,
        )


class ColumnIs(Generic[PyType]):
    """
    A class for using the IS operator

    #### Usage:
        ```python
        User.id.is_.true
        User.id.is_.false
        User.id.is_.null
        User.id.is_(True)
        ```
    """

    def __init__(self, column: Column[PyType]):
        self._column = column

    @property
    def not_(self) -> "ColumnIsNot":
        return ColumnIsNot(self._column)

    @property
    def null(self) -> IsCondition:
        return IsCondition(self._column)


class ColumnIsNot(Generic[PyType]):
    """
    A class for using the IS NOT operator

    #### Usage:
        ```python
        User.id.is_.not_.true
        User.id.is_.not_.false
        User.id.is_.not_.null
        User.id.is_.not_(True)
        ```
    """

    def __init__(self, column: Column[PyType]):
        self._column = column

    @property
    def null(self) -> "IsNotCondition":
        return IsNotCondition(self._column)


class ColumnNot(Generic[PyType]):
    """
    A class for using the NOT operator

    #### Usage:
        ```python
        User.id.not_.in_([1, 2, 3])
        ```
    """

    def __init__(self, column: Column[PyType]):
        self._column = column

    def in_(self, values: Sequence[PyType], /) -> NotInCondition:
        return NotInCondition(self._column, values)
