import pytest
import snowflake.connector.cursor
import snowman
import turu.snowflake
from pytest_mock import MockFixture
from snowman.schema.table import Table


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


@snowman.table("database", "schema", "users")
class User(Table):
    pass


@pytest.fixture
def user() -> User:
    return User()
