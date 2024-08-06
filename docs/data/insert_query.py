from snowman.query import insert
from your.snowflake import snowflake_conn

from docs.data.your.database.aaaschema import User

with snowflake_conn.cursor() as cursor:
    insert.into(User).values(
        User(
            id=1,
            name="John Doe",
        ),
    ).execute(cursor)
