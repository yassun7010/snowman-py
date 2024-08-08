from dataclasses import dataclass
from typing import Annotated, TypedDict

import pydantic
import pytest
import snowflake.connector.cursor
import snowman
from pydantic import Field
from pytest_mock import MockFixture
from snowman._features import USE_TURU
from snowman.query.column import Column
from snowman.relation.table import Table

if USE_TURU:
    import turu.snowflake  # type: ignore[import]


@pytest.fixture
def mock_snowflake_cursor(
    mocker: MockFixture,
) -> snowflake.connector.cursor.SnowflakeCursor:
    return mocker.MagicMock(spec=snowflake.connector.cursor.SnowflakeCursor)


@pytest.fixture
def mock_turu_snowflake_connection(
    mocker: MockFixture,
) -> "turu.snowflake.MockConnection":
    if USE_TURU:
        import turu.snowflake  # type: ignore[import]

        return turu.snowflake.MockConnection()

    else:
        return mocker.MagicMock(spec=snowflake.connector.connection.SnowflakeConnection)


@dataclass
class _UserAccessColumns:
    id: Column[int]
    name: Column[str]


class _UserInsertColumns(TypedDict):
    id: int
    name: str


class _UserUpdateColumns(TypedDict, total=False):
    id: int
    name: str


@snowman.table("database", "schema", "users")
class User(Table[_UserAccessColumns, _UserInsertColumns, _UserUpdateColumns]):
    id: int
    name: str


@snowman.table("DATABASE", "SCHEMA", "UPPERCASE_TABLE")
class UpperCaseTable(Table[_UserAccessColumns, _UserInsertColumns, _UserUpdateColumns]):
    model_config = pydantic.ConfigDict(populate_by_name=True)

    id: Annotated[int, Field(alias="ID")]
    name: Annotated[str, Field(alias="NAME")]


@dataclass
class _CompanyAccessColumns:
    id: Column[int]
    name: Column[str]


class _CompanyInsertColumns(TypedDict):
    id: int
    name: str


class _CompanyUpdateColumns(TypedDict, total=False):
    id: int
    name: str


@snowman.table("database", "schema", "companies")
class Company(
    Table[_CompanyAccessColumns, _CompanyInsertColumns, _CompanyUpdateColumns]
):
    id: int
    name: str


@pytest.fixture
def user() -> User:
    user = User(id=1, name="Alice")

    return user


@pytest.fixture
def uppercase_table() -> UpperCaseTable:
    return UpperCaseTable(id=1, name="Alice")


@pytest.fixture
def company() -> Company:
    company = Company(id=1, name="Apple")

    return company


@pytest.fixture
def int_column() -> Column[int]:
    return Column(
        int,
        database_name=User.__database_name__,
        schema_name=User.__schema_name__,
        table_name=User.__table_name__,
        column_name="id",
    )


@pytest.fixture
def int_nullable_column() -> Column[int | None]:
    return Column(
        int | None,  # type: ignore[valid-type]
        database_name=User.__database_name__,
        schema_name=User.__schema_name__,
        table_name=User.__table_name__,
        column_name="id",
    )
