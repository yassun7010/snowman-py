import pytest
import snowman.query
from conftest import REAL_TEST_IS_DESABLED, User
from snowflake.connector.connection import SnowflakeConnection
from snowman.query import select
from snowman.query.minify import minify


class TestSelectQueryBuilderBuild:
    def test_select_all(self):
        query, params = select().from_(User).build()
        assert query == minify(
            """
            SELECT
                *
            FROM
                database.schema.users
            """
        )
        assert params == ()

    # TODO: How to implement this?
    #
    # def test_select_specific_columns(self):
    #     query, params = select({"id": User.id, "name": "Alice"}).from_(User).build()
    #     assert query == "SELECT id, name FROM test_table"

    def test_select_with_where_clause(self):
        query, params = select().from_(User).where(lambda c: c.self.id > 18).build()

        assert query == minify(
            """
            SELECT
                *
            FROM
                database.schema.users
            WHERE
                id > %s
            """
        )
        assert params == (18,)

    def test_select_with_order_by(self):
        query, params = select().from_(User).order_by(lambda c: [c.self.name]).build()

        assert query == minify(
            """
            SELECT
                *
            FROM
                database.schema.users
            ORDER BY
                name
            """
        )
        assert params == ()

    def test_select_with_limit(self):
        query, params = select().from_(User).limit(10).build()

        assert query == "SELECT * FROM database.schema.users LIMIT %s"
        assert params == (10,)

    def test_select_with_multiple_conditions(self, user: User):
        query, params = (
            select()
            .from_(User)
            .where(lambda c: c.self.id > 18)
            .order_by(lambda c: c.self.name)
            .limit(5)
            .build()
        )

        assert query == minify(
            """
            SELECT
                *
            FROM
                database.schema.users
            WHERE
                id > %s
            ORDER BY
                name
            LIMIT
                %s
            """
        )
        assert params == (18, 5)


@pytest.mark.skipif(**REAL_TEST_IS_DESABLED)
class TestSelectQueryBuilderExecute:
    def test_select_all_execute_fetchall(
        self,
        real_user: User,
        snowflake_connection: SnowflakeConnection,
    ):
        from conftest import RealUser

        with snowflake_connection.cursor() as cursor:
            snowman.query.truncate(RealUser).execute(cursor)
            snowman.query.insert.into(RealUser).values(real_user).execute(cursor)
            users: list[User] = select().from_(RealUser).execute(cursor).fetchall()

            assert users == [real_user]

    def test_select_all_execute_fetchmany(
        self,
        real_user: User,
        snowflake_connection: SnowflakeConnection,
    ):
        from conftest import RealUser

        with snowflake_connection.cursor() as cursor:
            snowman.query.truncate(RealUser).execute(cursor)
            snowman.query.insert.into(RealUser).values(real_user).execute(cursor)
            users: list[User] = select().from_(RealUser).execute(cursor).fetchmany()

            assert users == [real_user]

    def test_select_all_execute_fetchone(
        self,
        real_user: User,
        snowflake_connection: SnowflakeConnection,
    ):
        from conftest import RealUser

        with snowflake_connection.cursor() as cursor:
            snowman.query.truncate(RealUser).execute(cursor)
            snowman.query.insert.into(RealUser).values(real_user).execute(cursor)
            user: User | None = select().from_(RealUser).execute(cursor).fetchone()

            assert user == real_user

    def test_select_all_execute_fetchone_when_none(
        self,
        real_user: User,
        snowflake_connection: SnowflakeConnection,
    ):
        from conftest import RealUser

        with snowflake_connection.cursor() as cursor:
            snowman.query.truncate(RealUser).execute(cursor)
            user: User | None = select().from_(RealUser).execute(cursor).fetchone()

            assert user is None

    def test_select_all_execute_fetchone_where_and_limit(
        self,
        real_user: User,
        snowflake_connection: SnowflakeConnection,
    ):
        from conftest import RealUser

        with snowflake_connection.cursor() as cursor:
            snowman.query.truncate(RealUser).execute(cursor)
            snowman.query.insert.into(RealUser).values(real_user).execute(cursor)

            user: User | None = (
                select()
                .from_(RealUser)
                .where(lambda c: c.self.id == 1)
                .limit(1)
                .execute(cursor)
                .fetchone()
            )

            assert user == real_user
