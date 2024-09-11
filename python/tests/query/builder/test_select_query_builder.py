import textwrap

import pytest
import snowman.query
from conftest import REAL_TEST_IS_DESABLED, User
from snowflake.connector.connection import SnowflakeConnection
from snowman.query import select


class TestSelectQueryBuilder:
    def test_select_all_build(self):
        query, params = select().from_(User).build()
        assert (
            query
            == textwrap.dedent(
                """
                SELECT
                    *
                FROM
                    database.schema.users
                """
            ).strip()
        )
        assert params == ()

    # def test_select_specific_columns(self):
    #     query, params = select({"id": User.id, "name": "Alice"}).from_(User).build()
    #     assert query == "SELECT id, name FROM test_table"

    def test_select_with_where_clause_build(self):
        query, params = select().from_(User).where(lambda c: c.self.id > 18).build()
        assert (
            query
            == textwrap.dedent(
                """
                SELECT
                    *
                FROM
                    database.schema.users
                WHERE
                    id > %s
                """
            ).strip()
        )
        assert params == (18,)

    # def test_select_with_order_by_build(self):
    #     query, params = select().from_(User).order_by(lambda c: c.self.name).build()
    #     assert query == "SELECT * FROM test_table ORDER BY name ASC"
    #     assert params == ()

    # def test_select_with_limit_build(self):
    #     query, params = select().from_(User).limit(10).build()
    #     assert query == "SELECT * FROM test_table LIMIT 10"
    #     assert params == ()

    # def test_select_with_multiple_conditions(self, user: User):
    #     query = (
    #         select()
    #         .from_(User)
    #         .where(lambda c: (c.self.id > 18) & (c.self.name.like("A%")))
    #         .order_by(lambda c: c.self.age.desc)
    #         .limit(5)
    #         .build()
    #     )
    #     assert (
    #         query
    #         == "SELECT name, age FROM test_table WHERE age > 18 AND name LIKE 'A%' ORDER BY age DESC LIMIT 5"
    #     )

    @pytest.mark.skipif(**REAL_TEST_IS_DESABLED)
    def test_select_all_execute_fetchall(
        self,
        real_user: User,
        snowflake_connection: SnowflakeConnection,
    ):
        from conftest import RealUser

        with snowflake_connection.cursor() as cursor:
            snowman.query.truncate(RealUser).execute(cursor)
            snowman.query.insert.into(RealUser).values(real_user).execute(cursor)
            users = select().from_(RealUser).execute(cursor).fetchall()

            assert users == [real_user]

    @pytest.mark.skipif(**REAL_TEST_IS_DESABLED)
    def test_select_all_execute_fetchmany(
        self,
        real_user: User,
        snowflake_connection: SnowflakeConnection,
    ):
        from conftest import RealUser

        with snowflake_connection.cursor() as cursor:
            snowman.query.truncate(RealUser).execute(cursor)
            snowman.query.insert.into(RealUser).values(real_user).execute(cursor)
            users = select().from_(RealUser).execute(cursor).fetchmany()

            assert users == [real_user]

    @pytest.mark.skipif(**REAL_TEST_IS_DESABLED)
    def test_select_all_execute_fetchone(
        self,
        real_user: User,
        snowflake_connection: SnowflakeConnection,
    ):
        from conftest import RealUser

        with snowflake_connection.cursor() as cursor:
            snowman.query.truncate(RealUser).execute(cursor)
            snowman.query.insert.into(RealUser).values(real_user).execute(cursor)
            user = select().from_(RealUser).execute(cursor).fetchone()

            assert user == real_user

    @pytest.mark.skipif(**REAL_TEST_IS_DESABLED)
    def test_select_all_execute_fetchone_when_none(
        self,
        real_user: User,
        snowflake_connection: SnowflakeConnection,
    ):
        from conftest import RealUser

        with snowflake_connection.cursor() as cursor:
            snowman.query.truncate(RealUser).execute(cursor)
            user = select().from_(RealUser).execute(cursor).fetchone()

            assert user is None
