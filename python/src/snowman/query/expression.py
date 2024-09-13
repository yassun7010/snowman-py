from typing import Type, cast

from snowman.relation.table import (
    GenericColumnAccessor,
    GenericInsertColumnTypedDict,
    GenericOrderItemAccessor,
    GenericUpdateColumnTypedDict,
    Table,
)
from snowman.relation.table_like import GenericTableLike
from snowman.relation.view import View

from .builder.condition.condition import Condition
from .builder.condition.group_condition import GroupCondition
from .column import _InternalColumnAccessor
from .order_item import _InternalOrderItemAccessor


def group(condition: Condition) -> GroupCondition:
    return GroupCondition(condition)


def column(
    table: Type[
        Table[
            GenericTableLike,
            GenericColumnAccessor,
            GenericOrderItemAccessor,
            GenericInsertColumnTypedDict,
            GenericUpdateColumnTypedDict,
        ]
        | View[GenericColumnAccessor, GenericOrderItemAccessor]
    ],
) -> GenericColumnAccessor:
    """
    Extract column information from the table.

    #### Usage:
        ```python
        repr(column(User).id) == "database.schema.users.id"
        ```
    """
    return cast(GenericColumnAccessor, _InternalColumnAccessor(table))


def order(
    table: Type[
        Table[
            GenericTableLike,
            GenericColumnAccessor,
            GenericOrderItemAccessor,
            GenericInsertColumnTypedDict,
            GenericUpdateColumnTypedDict,
        ]
        | View[GenericColumnAccessor, GenericOrderItemAccessor]
    ],
) -> GenericOrderItemAccessor:
    """
    Extract column information from the table.

    #### Usage:
        ```python
        repr(column(User).id) == "database.schema.users.id"
        ```
    """
    return cast(GenericOrderItemAccessor, _InternalOrderItemAccessor(table))
