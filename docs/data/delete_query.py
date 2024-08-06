from snowman.query import delete
from your.database.schema import User
from your.snowflake import snowflake_conn

with snowflake_conn.cursor() as cursor:
    delete.from_(User).where(
        "id = %s",
        [1],
    ).execute(cursor)
