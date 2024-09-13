#
# Code generated by snowman; DO NOT EDIT.
#
# For more information about snowman,
# please refer to https://github.com/yassun7010/snowman-py .
#

import dataclasses
import typing

import snowman

if typing.TYPE_CHECKING:
    from . import schema as schema


@dataclasses.dataclass(init=False, frozen=True, eq=False, order=False)
class _UserColumnAccessor:
    id: snowman.Column["schema.User", typing.Literal["id"], snowman.datatype.INTEGER]
    """User ID"""

    name: snowman.Column["schema.User", typing.Literal["name"], snowman.datatype.TEXT]
    """User Name"""

    age: snowman.Column[
        "schema.User", typing.Literal["age"], snowman.datatype.INTEGER | None
    ]
    """User Age"""

    created_at: snowman.Column[
        "schema.User", typing.Literal["created_at"], snowman.datatype.TIMESTAMP_TZ
    ]
    """Created At"""


@dataclasses.dataclass(init=False, frozen=True, eq=False, order=False)
class _UserOrderItemAccessor:
    id: snowman.ColumnOrderItem[
        "schema.User", typing.Literal["id"], snowman.datatype.INTEGER
    ]
    """User ID"""

    name: snowman.ColumnOrderItem[
        "schema.User", typing.Literal["name"], snowman.datatype.TEXT
    ]
    """User Name"""

    age: snowman.ColumnOrderItem[
        "schema.User", typing.Literal["age"], snowman.datatype.INTEGER | None
    ]
    """User Age"""

    created_at: snowman.ColumnOrderItem[
        "schema.User", typing.Literal["created_at"], snowman.datatype.TIMESTAMP_TZ
    ]
    """Created At"""


class _UserInsertTypedDict(typing.TypedDict):
    id: snowman.datatype.INTEGER
    """User ID"""

    name: snowman.datatype.TEXT
    """User Name"""

    age: typing.NotRequired[snowman.datatype.INTEGER | None]
    """User Age"""

    created_at: typing.NotRequired[snowman.datatype.TIMESTAMP_TZ]
    """Created At"""


class _UserUpdateTypedDict(typing.TypedDict):
    id: typing.NotRequired[snowman.datatype.INTEGER]
    """User ID"""

    name: typing.NotRequired[snowman.datatype.TEXT]
    """User Name"""

    age: typing.NotRequired[snowman.datatype.INTEGER | None]
    """User Age"""

    created_at: typing.NotRequired[snowman.datatype.TIMESTAMP_TZ]
    """Created At"""
