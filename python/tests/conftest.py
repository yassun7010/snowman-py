from typing import TypedDict

import pytest
import snowflake.connector.cursor
import snowq
import turu.snowflake
from pydantic import BaseModel
from pytest_mock import MockFixture
from snowq.schema.table import Table


@pytest.fixture
def mock_snowflake_cursor(
    mocker: MockFixture,
) -> snowflake.connector.cursor.SnowflakeCursor:
    return mocker.Mock(spec=snowflake.connector.cursor.SnowflakeCursor)


@pytest.fixture
def mock_turu_snowflake_connection(
    mocker: MockFixture,
) -> turu.snowflake.Connection:
    return mocker.Mock(spec=turu.snowflake.Connection)


@pytest.fixture
def mock_turu_snowflake_cursor(
    mocker: MockFixture,
) -> turu.snowflake.Cursor:
    return mocker.Mock(spec=turu.snowflake.Cursor)


class _UserInsertColumns(TypedDict):
    id: int
    name: str


class _UserUpdateColumns(TypedDict, total=False):
    id: int
    name: str


@snowq.table("database", "public", "users")
class User(BaseModel, Table[_UserInsertColumns, _UserUpdateColumns]):
    id: int
    name: str


@pytest.fixture
def user() -> User:
    user = User(id=1, name="Alice")

    return user
