import textwrap

import snowman
from conftest import User
from snowflake.connector.cursor import SnowflakeCursor


class TestDeleteQuery:
    def test_delete_query(self, user: User, mock_snowflake_cursor: SnowflakeCursor):
        snowman.query.delete.from_(User).where("id = 1").execute(mock_snowflake_cursor)

    def test_delete_query_build_using_condition(self):
        query, params = (
            snowman.query.delete.from_(User)
            .where(
                lambda c: (c(User).id == 1).and_(c(User).name == "Alice"),
            )
            .build()
        )

        assert (
            query
            == textwrap.dedent(
                """
                DELETE FROM
                    database.schema.users
                WHERE
                    id = %s
                    AND name = %s
                """
            ).strip()
        )

        assert params == (1, "Alice")

    def test_delete_query_build(self, user: User):
        query, params = snowman.query.delete.from_(User).where("id = %s", [1]).build()

        assert (
            query
            == textwrap.dedent(
                """
                DELETE FROM
                    database.schema.users
                WHERE
                    id = %s
                """
            ).strip()
        )

        assert params == (1,)
