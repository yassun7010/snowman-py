import pytest
import snowman
from conftest import REAL_TEST_IS_DESABLED, UpperCaseTable, User
from snowflake.connector.connection import SnowflakeConnection
from snowflake.connector.cursor import SnowflakeCursor
from snowman.query.expression import column as c
from snowman.query.minify import minify


class TestDeleteQuery:
    def test_delete_query(self, user: User, mock_snowflake_cursor: SnowflakeCursor):
        snowman.query.delete.from_(User).where("id = 1").execute(mock_snowflake_cursor)

    def test_delete_query_build_using_condition_callable(self):
        query, params = (
            snowman.query.delete.from_(User)
            .where(
                lambda c: (c.self.id == 1).and_(c.self.name == "Alice"),
            )
            .build()
        )

        assert query == minify(
            """
            DELETE FROM
                database.schema.users
            WHERE
                id = %s AND name = %s
            """
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

        assert query == minify(
            """
            DELETE FROM
                database.schema.users
            WHERE
                id = %s AND name = %s
            """
        )

        assert params == (1, "Alice")

    def test_delete_query_build(self, user: User):
        query, params = snowman.query.delete.from_(User).where("id = %s", [1]).build()

        assert query == minify(
            """
            DELETE FROM
                database.schema.users
            WHERE
                id = %s
            """
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

        assert query == minify(
            """
            DELETE FROM
                DATABASE.SCHEMA.UPPERCASE_TABLE
            WHERE
                ID = %s AND NAME = %s
            """
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

        assert query == minify(
            """
            DELETE FROM
                DATABASE.SCHEMA.UPPERCASE_TABLE
            WHERE
                ID = %s AND NAME = %s
            """
        )

        assert params == (1, "Alice")

    def test_delete_query_build(self):
        query, params = (
            snowman.query.delete.from_(UpperCaseTable).where("ID = %s", [1]).build()
        )

        assert query == minify(
            """
            DELETE FROM
                DATABASE.SCHEMA.UPPERCASE_TABLE
            WHERE
                ID = %s
            """
        )

        assert params == (1,)

    @pytest.mark.skipif(**REAL_TEST_IS_DESABLED)
    def test_real_delete_execute(
        self,
        real_user: User,
        snowflake_connection: SnowflakeConnection,
    ):
        from conftest import RealUser

        with snowflake_connection.cursor() as cursor:
            snowman.query.insert.into(RealUser).values(real_user).execute(cursor)
            snowman.query.delete.from_(RealUser).where(
                lambda c: c.self.id == real_user.id
            ).execute(cursor)
