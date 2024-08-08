import textwrap
from typing import TYPE_CHECKING

import pytest
import snowman
from conftest import UpperCaseTable, User
from snowflake.connector.cursor import SnowflakeCursor
from snowman._features import USE_TURU
from snowman.query.expression import column as c

if TYPE_CHECKING:
    import turu.snowflake


class TestUpdateQuery:
    def test_update_query(self, mock_snowflake_cursor: SnowflakeCursor):
        snowman.query.update(User).set({"id": 1, "name": "taro"}).where(
            "id = 1"
        ).execute(mock_snowflake_cursor)

    def test_update_query_dict_build(self):
        query, params = (
            snowman.query.update(User)
            .set({"name": "taro"})
            .where("id = %s", [1])
            .build()
        )

        assert (
            query
            == textwrap.dedent(
                """
                UPDATE
                    database.schema.users
                SET
                    name = %s
                WHERE
                    id = %s
                """
            ).strip()
        )
        assert params == ("taro", 1)

    def test_update_query_pydantic_build_using_condition_callable(self, user: User):
        query, params = (
            snowman.query.update(User)
            .set(user)
            .where(lambda c: (c(User).id == 1).and_(c(User).name != "Alice"))
            .build()
        )

        assert (
            query
            == textwrap.dedent(
                """
                UPDATE
                    database.schema.users
                SET
                    id = %s,
                    name = %s
                WHERE
                    id = %s AND name != %s
                """
            ).strip()
        )
        assert params == (1, "Alice", 1, "Alice")

    def test_update_query_pydantic_build_using_condition(self, user: User):
        query, params = (
            snowman.query.update(User)
            .set(user)
            .where((c(User).id == 1).and_(c(User).name != "Alice"))
            .build()
        )

        assert (
            query
            == textwrap.dedent(
                """
                UPDATE
                    database.schema.users
                SET
                    id = %s,
                    name = %s
                WHERE
                    id = %s AND name != %s
                """
            ).strip()
        )
        assert params == (1, "Alice", 1, "Alice")

    def test_update_query_pydantic_build(self, user: User):
        query, params = (
            snowman.query.update(User).set(user).where("id = %s", [1]).build()
        )

        assert (
            query
            == textwrap.dedent(
                """
                UPDATE
                    database.schema.users
                SET
                    id = %s,
                    name = %s
                WHERE
                    id = %s
                """
            ).strip()
        )
        assert params == (1, "Alice", 1)

    @pytest.mark.skipif(not USE_TURU, reason="Not installed turu")
    def test_insert_execute_by_turu(
        self,
        user: User,
        mock_turu_snowflake_connection: "turu.snowflake.MockConnection",
    ):
        from turu.core.tag import Update

        mock_turu_snowflake_connection.inject_operation_with_tag(Update[User])
        with mock_turu_snowflake_connection.cursor() as cursor:
            builder = snowman.query.update(User).set(user).where("id = %s", [1])
            builder.execute(cursor)


class TestUpdateQueryUpperCaseTable:
    def test_update_query_dict_build(self):
        query, params = (
            snowman.query.update(UpperCaseTable)
            .set({"name": "taro"})
            .where("ID = %s", [1])
            .build()
        )

        assert (
            query
            == textwrap.dedent(
                """
                UPDATE
                    DATABASE.SCHEMA.UPPERCASE_TABLE
                SET
                    NAME = %s
                WHERE
                    ID = %s
                """
            ).strip()
        )
        assert params == ("taro", 1)

    def test_update_query_pydantic_build_using_condition_callable(
        self, uppercase_table: UpperCaseTable
    ):
        query, params = (
            snowman.query.update(UpperCaseTable)
            .set(uppercase_table)
            .where(
                lambda c: (c(UpperCaseTable).id == 1).and_(
                    c(UpperCaseTable).name != "Alice"
                )
            )
            .build()
        )

        assert (
            query
            == textwrap.dedent(
                """
                UPDATE
                    DATABASE.SCHEMA.UPPERCASE_TABLE
                SET
                    ID = %s,
                    NAME = %s
                WHERE
                    ID = %s AND NAME != %s
                """
            ).strip()
        )
        assert params == (1, "Alice", 1, "Alice")

    def test_update_query_pydantic_build_using_condition(
        self, uppercase_table: UpperCaseTable
    ):
        query, params = (
            snowman.query.update(UpperCaseTable)
            .set(uppercase_table)
            .where((c(UpperCaseTable).id == 1).and_(c(UpperCaseTable).name != "Alice"))
            .build()
        )

        assert (
            query
            == textwrap.dedent(
                """
                UPDATE
                    DATABASE.SCHEMA.UPPERCASE_TABLE
                SET
                    ID = %s,
                    NAME = %s
                WHERE
                    ID = %s AND NAME != %s
                """
            ).strip()
        )
        assert params == (1, "Alice", 1, "Alice")

    def test_update_query_pydantic_build(self, uppercase_table: UpperCaseTable):
        query, params = (
            snowman.query.update(UpperCaseTable)
            .set(uppercase_table)
            .where("ID = %s", [1])
            .build()
        )

        assert (
            query
            == textwrap.dedent(
                """
                UPDATE
                    DATABASE.SCHEMA.UPPERCASE_TABLE
                SET
                    ID = %s,
                    NAME = %s
                WHERE
                    ID = %s
                """
            ).strip()
        )
        assert params == (1, "Alice", 1)
