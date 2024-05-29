import snowq
from conftest import User
from snowflake.connector.cursor import SnowflakeCursor


class TestTruncateQuery:
    def test_truncate_query(self, user: User, mock_snowflake_cursor: SnowflakeCursor):
        snowq.query.truncate.table(User).execute(mock_snowflake_cursor)

    def test_truncate_query_build(self, user: User):
        query, params = snowq.query.truncate(User).build()

        assert query == "TRUNCATE TABLE database.public.users"
        assert params == {}

    def test_truncate_if_exists_query_build(self, user: User):
        query, params = snowq.query.truncate.if_.exists(User).build()

        assert query == "TRUNCATE TABLE IF EXISTS database.public.users"
        assert params == {}

    def test_truncate_table_query_build(self, user: User):
        query, params = snowq.query.truncate.table(User).build()

        assert query == "TRUNCATE TABLE database.public.users"
        assert params == {}

    def test_truncate_table_if_exists_query_build(self, user: User):
        query, params = snowq.query.truncate.table.if_.exists(User).build()

        assert query == "TRUNCATE TABLE IF EXISTS database.public.users"
        assert params == {}
