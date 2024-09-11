import os
from dataclasses import dataclass
from typing import Annotated, Final, LiteralString, TypedDict, cast

import pydantic
import pytest
import snowflake.connector.cursor
import snowman
from pydantic import Field
from pytest_mock import MockFixture
from snowman._features import USE_TURU
from snowman.query.column import Column
from snowman.relation.table import Table
from turu.snowflake.features import USE_PANDAS, USE_PYARROW

if USE_TURU:
    import turu.snowflake  # type: ignore[import]

REAL_TEST_ENABLED = (
    os.getenv("REAL_TEST_ENABLED") == "true"
    and os.getenv("REAL_TEST_USER_DATABASE_NAME")
    and os.getenv("REAL_TEST_USER_SCHEMA_NAME")
    and os.getenv("REAL_TEST_USER_TABLE_NAME")
)


class SkipCondition(TypedDict):
    condition: bool
    reason: str


TURU_NOT_INSTALLED: Final[SkipCondition] = {
    "condition": not USE_TURU,
    "reason": "Not installed turu",
}

PANDAS_NOT_INSTALLED: Final[SkipCondition] = {
    "condition": not USE_PANDAS,
    "reason": "Not installed pandas",
}

PYARROW_NOT_INSTALLED: Final[SkipCondition] = {
    "condition": not USE_PYARROW,
    "reason": "Not installed pyarrow",
}

REAL_TEST_IS_DESABLED: Final[SkipCondition] = {
    "condition": not REAL_TEST_ENABLED,
    "reason": "Real test is disabled",
}


@pytest.fixture
def mock_snowflake_cursor(
    mocker: MockFixture,
) -> snowflake.connector.cursor.SnowflakeCursor:
    return mocker.MagicMock(spec=snowflake.connector.cursor.SnowflakeCursor)


@pytest.fixture
def snowflake_connection() -> snowflake.connector.connection.SnowflakeConnection:
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
    )


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
class _UserColumnsAccessor:
    id: Column[int]
    name: Column[str]


class _UserInsertColumns(TypedDict):
    id: int
    name: str


class _UserUpdateColumns(TypedDict, total=False):
    id: int
    name: str


@snowman.table("database", "schema", "users")
class User(Table["User", _UserColumnsAccessor, _UserInsertColumns, _UserUpdateColumns]):
    id: int
    name: str


@pytest.fixture
def user() -> User:
    user = User(id=1, name="Alice")

    return user


@snowman.table("DATABASE", "SCHEMA", "UPPERCASE_TABLE")
class UpperCaseTable(
    Table[
        "UpperCaseTable", _UserColumnsAccessor, _UserInsertColumns, _UserUpdateColumns
    ]
):
    model_config = pydantic.ConfigDict(populate_by_name=True)

    id: Annotated[int, Field(alias="ID")]
    name: Annotated[str, Field(alias="NAME")]


@pytest.fixture
def uppercase_table() -> UpperCaseTable:
    return UpperCaseTable(id=1, name="Alice")


if REAL_TEST_ENABLED:

    @snowman.table(
        cast(LiteralString, os.environ["REAL_TEST_USER_DATABASE_NAME"]),
        cast(LiteralString, os.environ["REAL_TEST_USER_SCHEMA_NAME"]),
        cast(LiteralString, os.environ["REAL_TEST_USER_TABLE_NAME"]),
    )
    class RealUser(User):
        pass

    @pytest.fixture
    def real_user() -> User:
        return RealUser(id=1, name="Alice")


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
    Table[
        "Company", _CompanyAccessColumns, _CompanyInsertColumns, _CompanyUpdateColumns
    ]
):
    id: int
    name: str


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
