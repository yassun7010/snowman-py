from snowman.query import update
from your.database.schema import User
from your.snowflake import snowflake_conn

with snowflake_conn.cursor() as cursor:
    update(User).set(
        {"name": "Jane Doe"},
    ).where(
        "id = %s",
        [1],
    ).execute(cursor)
