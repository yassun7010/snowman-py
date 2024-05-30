from typing import TypedDict

import pydantic
import snowq


class _UserInsertColumns(TypedDict):
    id: int
    name: str


class _UserUpdateColumns(TypedDict, total=False):
    id: int
    name: str


@snowq.table("database", "public", "users")
class User(pydantic.BaseModel, snowq.Table["_UserInsertColumns", "_UserUpdateColumns"]):
    id: int
    name: str
