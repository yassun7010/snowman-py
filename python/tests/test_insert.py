import textwrap

import pytest
import snowq
import snowq.exception
from conftest import User
from snowflake.connector.cursor import SnowflakeCursor
from snowq._features import USE_PANDAS


class TestInsertQuery:
    def test_insert_execute_by_snowflake_cursor(
        self, user: User, mock_snowflake_cursor: SnowflakeCursor
    ):
        snowq.query.insert.into(User).values(user).execute(mock_snowflake_cursor)

    def test_insert_execute_by_turu_connection(
        self, user: User, mock_turu_snowflake_connection
    ):
        snowq.query.insert.into(User).values(user).execute(
            mock_turu_snowflake_connection
        )

    def test_insert_execute_by_turu_cursor(
        self, user: User, mock_turu_snowflake_cursor
    ):
        snowq.query.insert.into(User).values(user).execute(mock_turu_snowflake_cursor)

    def test_insert_into_query_execute_build(self, user: User):
        query, params = snowq.query.insert.into(User).values(user).build()

        assert (
            query
            == textwrap.dedent(
                """
                INSERT INTO
                    database.public.users
                VALUES (
                    %(id)s,
                    %(name)s
                )
                """
            ).strip()
        )
        assert params == user.model_dump()

    def test_insert_into_query_execute_many_build(self, user: User):
        values = [user, user]
        query, params = snowq.query.insert.into(User).values(values).build()

        assert (
            query
            == textwrap.dedent(
                """
                INSERT INTO
                    database.public.users
                VALUES (
                    %(id)s,
                    %(name)s
                )
                """
            ).strip()
        )
        assert params == tuple(value.model_dump() for value in values)

    def test_insert_into_query_overwrite_execute_build(self, user: User):
        query, params = snowq.query.insert.overwrite.into(User).values(user).build()

        assert (
            query
            == textwrap.dedent(
                """
                INSERT OVERWRITE INTO
                    database.public.users
                VALUES (
                    %(id)s,
                    %(name)s
                )
                """
            ).strip()
        )
        assert params == user.model_dump()

    @pytest.mark.skipif(not USE_PANDAS, reason="Not installed pandas")
    def test_insert_into_query_build_use_dataframe(self):
        import pandas as pd

        with pytest.raises(snowq.exception.SnowqNotDataFrameAvailableError):
            snowq.query.insert.into(User).values(pd.DataFrame()).build()

    @pytest.mark.skipif(not USE_PANDAS, reason="Not installed pandas")
    def test_insert_into_query_execute_use_dataframe(
        self, mock_snowflake_cursor: SnowflakeCursor
    ):
        import pandas as pd

        snowq.query.insert.into(User).values(
            pd.DataFrame(
                {
                    "id": list(range(5)),
                    "name": [f"name_{i}" for i in range(5)],
                }
            )
        ).execute(mock_snowflake_cursor)
