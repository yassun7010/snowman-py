import textwrap

import snowman
from conftest import User
from snowflake.connector.cursor import SnowflakeCursor


class TestInsertInto:
    def test_insert_execute_by_snowflake_cursor(
        self, user: User, mock_snowflake_cursor: SnowflakeCursor
    ):
        snowman.query.insert.into(User).values(user, user).execute(
            mock_snowflake_cursor
        )

    def test_insert_execute_by_turu_connection(
        self, user: User, mock_turu_snowflake_connection
    ):
        snowman.query.insert.into(User).values(user, user).execute(
            mock_turu_snowflake_connection
        )

    def test_insert_execute_by_turu_cursor(
        self, user: User, mock_turu_snowflake_cursor
    ):
        snowman.query.insert.into(User).values(user, user).execute(
            mock_turu_snowflake_cursor
        )

    def test_insert_into_query_build(self, user: User):
        query, params = snowman.query.insert.into(User).values(user, user).build()

        assert (
            query
            == textwrap.dedent(
                """
                INSERT INTO
                    <class 'conftest.User'>
                VALUES (
                    ?, ?
                )
                """
            ).strip()
        )
        assert params == {}
