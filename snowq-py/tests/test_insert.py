import textwrap

import snowq
from conftest import User
from snowflake.connector.cursor import SnowflakeCursor


class TestInsertQuery:
    def test_insert_execute_by_snowflake_cursor(
        self, user: User, mock_snowflake_cursor: SnowflakeCursor
    ):
        snowq.query.insert.into(User).values(user, user).execute(mock_snowflake_cursor)

    def test_insert_execute_by_turu_connection(
        self, user: User, mock_turu_snowflake_connection
    ):
        snowq.query.insert.into(User).values(user, user).execute(
            mock_turu_snowflake_connection
        )

    def test_insert_execute_by_turu_cursor(
        self, user: User, mock_turu_snowflake_cursor
    ):
        snowq.query.insert.into(User).values(user, user).execute(
            mock_turu_snowflake_cursor
        )

    def test_insert_into_query_build(self, user: User):
        query, params = snowq.query.insert.into(User).values(user, user).build()

        assert (
            query
            == textwrap.dedent(
                """
                INSERT INTO
                    database.public.users
                VALUES (
                    ?, ?
                )
                """
            ).strip()
        )
        assert params == {}
