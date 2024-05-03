import pytest
import snowflake.connector.cursor
import snowq
import turu.snowflake
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


@snowq.table("database", "schema", "users")
class User(Table):
    pass


@pytest.fixture
def user() -> User:
    return User()
