import textwrap
import snowq
from conftest import User
from snowflake.connector.cursor import SnowflakeCursor


class TestUpdateStatement:
    def test_update_statement(self, user: User, mock_snowflake_cursor: SnowflakeCursor):
        snowq.query.update(User).set(**user.model_dump()).execute(mock_snowflake_cursor)

    def test_update_query_build(self, user: User):
        query, params = snowq.query.update(User).set(**user.model_dump()).build()

        assert (
            query
            == textwrap.dedent(
                """
                UPDATE
                    database.public.users
                SET
                    id = %(id)s
                    name = %(name)s
                """
            ).strip()
        )
        assert params == user.model_dump()
