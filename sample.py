import typing
from typing import TypedDict

import pydantic
import snowman

pydantic.Json


class UserInsertTypedDict(TypedDict):
    id: int
    name: str


class UserUpdateTypedDict(TypedDict):
    id: typing.NotRequired[int]
    name: typing.NotRequired[str]


class User(
    pydantic.BaseModel, snowman.PydanticTable[UserInsertTypedDict, UserUpdateTypedDict]
):
    id: snowman.Column[int]
    name: snowman.Column[str]


# User.id.is_.not_()
# User.name

user = User(id=123, name="Alice")
user.id
user.name
