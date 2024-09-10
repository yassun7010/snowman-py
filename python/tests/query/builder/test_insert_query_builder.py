import textwrap

import pytest
import snowman
import snowman.exception
from conftest import (
    PANDAS_NOT_INSTALLED,
    REAL_TEST_IS_DESABLED,
    TURU_NOT_INSTALLED,
    UpperCaseTable,
    User,
)
from snowflake.connector.connection import SnowflakeConnection
from snowflake.connector.cursor import SnowflakeCursor
from snowman._features import USE_TURU

if USE_TURU:
    import turu.snowflake  # type: ignore[import]


class TestInsertQuery:
    def test_insert_execute_by_snowflake_cursor(
        self, user: User, mock_snowflake_cursor: SnowflakeCursor
    ):
        builder = snowman.query.insert.into(User).values(user)
        builder.execute(mock_snowflake_cursor)
        assert builder._use_execute_many is False

    def test_insert_executemany_by_snowflake_cursor(
        self, user: User, mock_snowflake_cursor: SnowflakeCursor
    ):
        builder = snowman.query.insert.into(User).values([user, user])
        builder.execute(mock_snowflake_cursor)
        assert builder._use_execute_many is True

    def test_insert_execute_when_typed_dict(
        self, mock_snowflake_cursor: SnowflakeCursor
    ):
        builder = snowman.query.insert.into(User).values({"id": 1, "name": "Alice"})
        builder.execute(mock_snowflake_cursor)
        assert builder._use_execute_many is False

    def test_insert_executemany_when_typed_dict(
        self, mock_snowflake_cursor: SnowflakeCursor
    ):
        builder = snowman.query.insert.into(User).values(
            [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"},
            ]
        )
        builder.execute(mock_snowflake_cursor)
        assert builder._use_execute_many is True

    @pytest.mark.skipif(**TURU_NOT_INSTALLED)
    def test_insert_execute_by_turu(
        self,
        user: User,
        mock_turu_snowflake_connection: "turu.snowflake.MockConnection",
    ):
        from turu.core.tag import Insert

        mock_turu_snowflake_connection.inject_operation_with_tag(Insert[User])
        with mock_turu_snowflake_connection.cursor() as cursor:
            builder = snowman.query.insert.into(User).values(user)
            builder.execute(cursor)

            assert builder._use_execute_many is False

    @pytest.mark.skipif(**TURU_NOT_INSTALLED)
    def test_insert_executemany_by_turu(
        self,
        user: User,
        mock_turu_snowflake_connection: "turu.snowflake.MockConnection",
    ):
        from turu.core.tag import Insert

        mock_turu_snowflake_connection.inject_operation_with_tag(Insert[User])
        with mock_turu_snowflake_connection.cursor() as cursor:
            builder = snowman.query.insert.into(User).values([user, user])
            builder.execute(cursor)

            assert builder._use_execute_many is True

    def test_insert_into_query_execute_build(self, user: User):
        query, params = snowman.query.insert.into(User).values(user).build()

        assert (
            query
            == textwrap.dedent(
                """
                INSERT INTO
                    database.schema.users
                (
                    id,
                    name
                )
                VALUES (
                    %s,
                    %s
                )
                """
            ).strip()
        )
        assert params == (1, "Alice")

    def test_insert_into_query_execute_many_build(self, user: User):
        values = [user, user]
        query, params = snowman.query.insert.into(User).values(values).build()

        assert (
            query
            == textwrap.dedent(
                """
                INSERT INTO
                    database.schema.users
                (
                    id,
                    name
                )
                VALUES (
                    %s,
                    %s
                )
                """
            ).strip()
        )
        assert params == ((1, "Alice"), (1, "Alice"))

    def test_insert_into_query_overwrite_execute_build(self, user: User):
        query, params = snowman.query.insert.overwrite.into(User).values(user).build()

        assert (
            query
            == textwrap.dedent(
                """
                INSERT OVERWRITE INTO
                    database.schema.users
                (
                    id,
                    name
                )
                VALUES (
                    %s,
                    %s
                )
                """
            ).strip()
        )
        assert params == (1, "Alice")

    @pytest.mark.skipif(**PANDAS_NOT_INSTALLED)
    def test_insert_into_query_build_use_dataframe(self):
        import pandas as pd

        with pytest.raises(snowman.exception.snowmanNotDataFrameAvailableError):
            snowman.query.insert.into(User).values(pd.DataFrame()).build()

    @pytest.mark.skipif(**PANDAS_NOT_INSTALLED)
    def test_insert_into_query_execute_use_dataframe(
        self, mock_snowflake_cursor: SnowflakeCursor
    ):
        import pandas as pd

        snowman.query.insert.into(User).values(
            pd.DataFrame(
                {
                    "id": list(range(5)),
                    "name": [f"name_{i}" for i in range(5)],
                }
            )
        ).execute(mock_snowflake_cursor)

    @pytest.mark.skipif(**TURU_NOT_INSTALLED)
    @pytest.mark.skipif(**PANDAS_NOT_INSTALLED)
    @pytest.mark.xfail(reason="turu.snowflake.MockCursor does not have connection.")
    def test_insert_into_query_execute_use_dataframe_and_turu(
        self, mock_turu_snowflake_connection: "turu.snowflake.MockConnection"
    ):
        import pandas as pd

        mock_turu_snowflake_connection.inject_response(None, None)

        with mock_turu_snowflake_connection.cursor() as cursor:
            snowman.query.insert.into(User).values(
                pd.DataFrame(
                    {
                        "id": list(range(5)),
                        "name": [f"name_{i}" for i in range(5)],
                    }
                )
            ).execute(cursor)

    @pytest.mark.skipif(**REAL_TEST_IS_DESABLED)
    def test_real_insert_execute(
        self,
        real_user: User,
        snowflake_connection: SnowflakeConnection,
    ):
        from conftest import RealUser

        with snowflake_connection.cursor() as cursor:
            snowman.query.insert.into(RealUser).values(real_user).execute(cursor)


class TestInsertQueryUpperCaseTable:
    def test_insert_into_query_execute_build(self, uppercase_table: UpperCaseTable):
        query, params = (
            snowman.query.insert.into(UpperCaseTable).values(uppercase_table).build()
        )

        assert (
            query
            == textwrap.dedent(
                """
                INSERT INTO
                    DATABASE.SCHEMA.UPPERCASE_TABLE
                (
                    ID,
                    NAME
                )
                VALUES (
                    %s,
                    %s
                )
                """
            ).strip()
        )
        assert params == (1, "Alice")

    def test_insert_into_query_execute_many_build(
        self, uppercase_table: UpperCaseTable
    ):
        values = [uppercase_table, uppercase_table]
        query, params = snowman.query.insert.into(UpperCaseTable).values(values).build()

        assert (
            query
            == textwrap.dedent(
                """
                INSERT INTO
                    DATABASE.SCHEMA.UPPERCASE_TABLE
                (
                    ID,
                    NAME
                )
                VALUES (
                    %s,
                    %s
                )
                """
            ).strip()
        )
        assert params == ((1, "Alice"), (1, "Alice"))

    def test_insert_into_query_overwrite_execute_build(
        self, uppercase_table: UpperCaseTable
    ):
        query, params = (
            snowman.query.insert.overwrite.into(UpperCaseTable)
            .values(uppercase_table)
            .build()
        )

        assert (
            query
            == textwrap.dedent(
                """
                INSERT OVERWRITE INTO
                    DATABASE.SCHEMA.UPPERCASE_TABLE
                (
                    ID,
                    NAME
                )
                VALUES (
                    %s,
                    %s
                )
                """
            ).strip()
        )
        assert params == (1, "Alice")
