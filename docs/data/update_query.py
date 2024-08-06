from snowman.query import update
from your.snowflake import snowflake_conn

from docs.data.your.database.aaaschema import User

with snowflake_conn.cursor() as cursor:
    update(User).set(
        {"name": "Jane Doe"},
    ).where(
        "id = %s",
        [1],
    ).execute(cursor)
