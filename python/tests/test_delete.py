import textwrap

import snowman
from conftest import User
from snowflake.connector.cursor import SnowflakeCursor


class TestDeleteQuery:
    def test_delete_query(self, user: User, mock_snowflake_cursor: SnowflakeCursor):
        snowman.query.delete.from_(User).where("id = 1").execute(mock_snowflake_cursor)

    def test_delete_query_build(self, user: User):
        query, params = snowman.query.delete.from_(User).where("id = 1").build()

        assert (
            query
            == textwrap.dedent(
                """
                DELETE FROM
                    database.public.users
                WHERE
                    id = 1
                """
            ).strip()
        )

        assert params == ()
