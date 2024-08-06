import textwrap
from typing import TYPE_CHECKING

import pytest
import snowman
from conftest import User
from snowflake.connector.cursor import SnowflakeCursor
from snowman._features import USE_TURU

if TYPE_CHECKING:
    import turu.snowflake


class TestUpdateQuery:
    def test_update_query(self, user: User, mock_snowflake_cursor: SnowflakeCursor):
        snowman.query.update(User).set({"id": 1, "name": "taro"}).where(
            "id = 1"
        ).execute(mock_snowflake_cursor)

    def test_update_query_dict_build(
        self, user: User, mock_snowflake_cursor: SnowflakeCursor
    ):
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
                    database.public.users
                SET
                    name = %s
                WHERE
                    id = %s
                """
            ).strip()
        )
        assert params == ("taro", 1)

    def test_update_query_pydantic_build(self, user: User):
        query, params = (
            snowman.query.update(User).set(user).where("id = %s", [1]).build()
        )

        assert (
            query
            == textwrap.dedent(
                """
                UPDATE
                    database.public.users
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
