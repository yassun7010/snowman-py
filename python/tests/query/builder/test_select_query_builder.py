import textwrap

import pytest
import snowman.query
from conftest import REAL_TEST_IS_DESABLED, User
from snowflake.connector.connection import SnowflakeConnection


class TestSelectQueryBuilder:
    def test_select_all_build(self):
        query, params = snowman.query.select().from_(User).build()
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

    @pytest.mark.skipif(**REAL_TEST_IS_DESABLED)
    def test_select_all_execute(
        self,
        real_user: User,
        snowflake_connection: SnowflakeConnection,
    ):
        from conftest import RealUser

        with snowflake_connection.cursor() as cursor:
            snowman.query.truncate(RealUser).execute(cursor)
            snowman.query.insert.into(RealUser).values(real_user).execute(cursor)
            users = snowman.query.select().from_(RealUser).execute(cursor).fetchall()

            assert users


# def test_select_specific_columns():
#     query = select().from_(TestTable).columns(TestTable.id, TestTable.name).build()
#     assert query == "SELECT id, name FROM test_table"


# def test_select_with_where():
#     query = select().from_(TestTable).where(TestTable.age > 18).build()
#     assert query == "SELECT * FROM test_table WHERE age > 18"


# def test_select_with_order_by():
#     query = select().from_(TestTable).order_by(TestTable.name.asc()).build()
#     assert query == "SELECT * FROM test_table ORDER BY name ASC"


# def test_select_with_limit():
#     query = select().from_(TestTable).limit(10).build()
#     assert query == "SELECT * FROM test_table LIMIT 10"


# def test_select_with_multiple_conditions(user: User):
#     query = (
#         select()
#         .from_(TestTable)
#         .where(lambda c: (c.self.age > 18) & (c.self.name.like("A%")))
#         .order_by(lambda c: c.self.age.desc)
#         .limit(5)
#         .build()
#     )
#     assert (
#         query
#         == "SELECT name, age FROM test_table WHERE age > 18 AND name LIKE 'A%' ORDER BY age DESC LIMIT 5"
#     )
