import textwrap

import snowman
from conftest import User
from snowflake.connector.cursor import SnowflakeCursor


class TestUpdateQuery:
    def test_update_query(self, user: User, mock_snowflake_cursor: SnowflakeCursor):
        snowman.query.update(User).set({"id": 1, "name": "taro"}).where("id = 1").execute(
            mock_snowflake_cursor
        )

    def test_update_query_dict_build(
        self, user: User, mock_snowflake_cursor: SnowflakeCursor
    ):
        query, params = (
            snowman.query.update(User).set({"name": "taro"}).where("id = 1").build()
        )

        assert (
            query
            == textwrap.dedent(
                """
                UPDATE
                    database.public.users
                SET
                    name = %(name)s
                WHERE
                    id = 1
                """
            ).strip()
        )
        assert params == {"name": "taro"}

    def test_update_query_pydantic_build(self, user: User):
        query, params = snowman.query.update(User).set(user).where("id = 1").build()

        assert (
            query
            == textwrap.dedent(
                """
                UPDATE
                    database.public.users
                SET
                    id = %(id)s,
                    name = %(name)s
                WHERE
                    id = 1
                """
            ).strip()
        )
        assert params == user.model_dump()
