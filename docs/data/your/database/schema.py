from typing import TypedDict

import pydantic
import snowman


class _UserInsertColumns(TypedDict):
    id: int
    name: str


class _UserUpdateColumns(TypedDict, total=False):
    id: int
    name: str


@snowman.table("database", "schema", "users")
class User(
    pydantic.BaseModel, snowman.Table["_UserInsertColumns", "_UserUpdateColumns"]
):
    id: int
    name: str
