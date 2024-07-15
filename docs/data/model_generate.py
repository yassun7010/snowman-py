#
# Code generated by snowman; DO NOT EDIT.
#
# For more information about snowman,
# please refer to https://github.com/yassun7010/snowman-py .
#

import datetime
import typing

import pydantic
import snowman

if typing.TYPE_CHECKING:
    from . import _schema as _schema


# TABLE: DATABASE.SCHEMA.USER
@snowman.table("DATABASE", "SCHEMA", "USER")
class User(
    pydantic.BaseModel,
    snowman.Table["_schema._UserInsertTypedDict", "_schema._UserUpdateTypedDict"],
):
    """User Table"""

    model_config = pydantic.ConfigDict(populate_by_name=True)

    id: typing.Annotated[
        snowman.datatype.INTEGER, pydantic.Field(title="User ID", alias="ID")
    ]
    """User ID"""

    name: typing.Annotated[
        snowman.datatype.TEXT, pydantic.Field(title="User Name", alias="NAME")
    ]
    """User Name"""

    age: typing.Annotated[
        snowman.datatype.INTEGER | None, pydantic.Field(title="User Age", alias="AGE")
    ] = None
    """User Age"""

    created_at: typing.Annotated[
        snowman.datatype.TIMESTAMP_TZ,
        pydantic.Field(title="Created At", alias="CREATED_AT"),
    ] = snowman.pydantic.DefaultFactory(datetime.datetime.now)
    """Created At"""
