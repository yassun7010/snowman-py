from typing import Type, cast

from snowman.relation.table import (
    GenericColumnAccessor,
    GenericInsertColumnTypedDict,
    GenericUpdateColumnTypedDict,
    Table,
)

from .builder.condition.condition import Condition
from .builder.condition.group_condition import GroupCondition
from .column import _InternalColumnAccessor


def group(condition: Condition) -> GroupCondition:
    return GroupCondition(condition)


def column(
    table: Type[
        Table[
            GenericColumnAccessor,
            GenericInsertColumnTypedDict,
            GenericUpdateColumnTypedDict,
        ]
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
