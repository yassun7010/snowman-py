from typing import TYPE_CHECKING

import pytest
import snowman
from conftest import REAL_TEST_IS_DESABLED, TURU_NOT_INSTALLED, User
from snowflake.connector.connection import SnowflakeConnection
from snowflake.connector.cursor import SnowflakeCursor

if TYPE_CHECKING:
    import turu.snowflake


class TestTruncateQuery:
    def test_truncate_query(self, user: User, mock_snowflake_cursor: SnowflakeCursor):
        snowman.query.truncate.table(User).execute(mock_snowflake_cursor)

    def test_truncate_query_build(self, user: User):
        query, params = snowman.query.truncate(User).build()

        assert query == "TRUNCATE TABLE database.schema.users"
        assert params == ()

    def test_truncate_if_exists_query_build(self, user: User):
        query, params = snowman.query.truncate.if_.exists(User).build()

        assert query == "TRUNCATE TABLE IF EXISTS database.schema.users"
        assert params == ()

    def test_truncate_table_query_build(self, user: User):
        query, params = snowman.query.truncate.table(User).build()

        assert query == "TRUNCATE TABLE database.schema.users"
        assert params == ()

    def test_truncate_table_if_exists_query_build(self, user: User):
        query, params = snowman.query.truncate.table.if_.exists(User).build()

        assert query == "TRUNCATE TABLE IF EXISTS database.schema.users"
        assert params == ()

    @pytest.mark.skipif(**TURU_NOT_INSTALLED)
    def test_insert_execute_by_turu(
        self,
        user: User,
        mock_turu_snowflake_connection: "turu.snowflake.MockConnection",
    ):
        from turu.core.tag import Truncate

        mock_turu_snowflake_connection.inject_operation_with_tag(Truncate[User])
        with mock_turu_snowflake_connection.cursor() as cursor:
            builder = snowman.query.truncate(User)
            builder.execute(cursor)

    @pytest.mark.skipif(**REAL_TEST_IS_DESABLED)
    def test_real_truncate_execute(
        self,
        snowflake_connection: SnowflakeConnection,
    ):
        from conftest import RealUser

        with snowflake_connection.cursor() as cursor:
            snowman.query.truncate(RealUser).execute(cursor)
