import textwrap

import snowman
from conftest import UpperCaseTable, User
from snowflake.connector.cursor import SnowflakeCursor
from snowman.query.expression import column as c


class TestDeleteQuery:
    def test_delete_query(self, user: User, mock_snowflake_cursor: SnowflakeCursor):
        snowman.query.delete.from_(User).where("id = 1").execute(mock_snowflake_cursor)

    def test_delete_query_build_using_condition_callable(self):
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
                    id = %s AND name = %s
                """
            ).strip()
        )

        assert params == (1, "Alice")

    def test_delete_query_build_using_condition(self):
        query, params = (
            snowman.query.delete.from_(User)
            .where(
                (c(User).id == 1).and_(c(User).name == "Alice"),
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
                    id = %s AND name = %s
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


class TestDeleteQueryUpperCaseTable:
    def test_delete_query(self, mock_snowflake_cursor: SnowflakeCursor):
        snowman.query.delete.from_(UpperCaseTable).where("id = 1").execute(
            mock_snowflake_cursor
        )

    def test_delete_query_build_using_condition_callable(self):
        query, params = (
            snowman.query.delete.from_(UpperCaseTable)
            .where(
                lambda c: (c(UpperCaseTable).id == 1).and_(
                    c(UpperCaseTable).name == "Alice"
                ),
            )
            .build()
        )

        assert (
            query
            == textwrap.dedent(
                """
                DELETE FROM
                    DATABASE.SCHEMA.UPPERCASE_TABLE
                WHERE
                    ID = %s AND NAME = %s
                """
            ).strip()
        )

        assert params == (1, "Alice")

    def test_delete_query_build_using_condition(self):
        query, params = (
            snowman.query.delete.from_(UpperCaseTable)
            .where(
                (c(UpperCaseTable).id == 1).and_(c(UpperCaseTable).name == "Alice"),
            )
            .build()
        )

        assert (
            query
            == textwrap.dedent(
                """
                DELETE FROM
                    DATABASE.SCHEMA.UPPERCASE_TABLE
                WHERE
                    ID = %s AND NAME = %s
                """
            ).strip()
        )

        assert params == (1, "Alice")

    def test_delete_query_build(self):
        query, params = (
            snowman.query.delete.from_(UpperCaseTable).where("ID = %s", [1]).build()
        )

        assert (
            query
            == textwrap.dedent(
                """
                DELETE FROM
                    DATABASE.SCHEMA.UPPERCASE_TABLE
                WHERE
                    ID = %s
                """
            ).strip()
        )

        assert params == (1,)
