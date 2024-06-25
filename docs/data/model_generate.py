#
# Code generated by snowman; DO NOT EDIT.
#
# For more information about snowman,
# please refer to https://github.com/yassun7010/snowman-py .
#

import typing

import pydantic
import snowman

if typing.TYPE_CHECKING:

    class _UserInsertTypedDict(typing.TypedDict):
        id: snowman.datatype.INTEGER
        """User ID"""

        name: snowman.datatype.TEXT
        """User Name"""

        created_at: typing.NotRequired[snowman.datatype.TIMESTAMP]
        """Created At"""

    class _UserUpdateTypedDict(typing.TypedDict):
        id: typing.NotRequired[snowman.datatype.INTEGER]
        """User ID"""

        name: typing.NotRequired[snowman.datatype.TEXT]
        """User Name"""

        created_at: typing.NotRequired[snowman.datatype.TIMESTAMP]
        """Created At"""


# TABLE: DATABASE.SCHEMA.USER
@snowman.table("DATABASE", "SCHEMA", "USER")
class User(
    pydantic.BaseModel,
    snowman.Table[
        "_UserInsertTypedDict",
        "_UserUpdateTypedDict",
    ],
):
    """User Table"""

    model_config = pydantic.ConfigDict(populate_by_name=True)

    id: typing.Annotated[
        snowman.datatype.INTEGER,
        pydantic.Field(title="User ID", alias="ID"),
    ]
    """User ID"""

    name: typing.Annotated[
        snowman.datatype.TEXT,
        pydantic.Field(title="User Name", alias="NAME"),
    ]
    """User Name"""

    created_at: typing.Annotated[
        snowman.datatype.TIMESTAMP,
        pydantic.Field(title="Created At", alias="CREATED_AT"),
    ]
    """Created At"""
