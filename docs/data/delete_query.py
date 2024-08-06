from snowman.query import delete
from your.snowflake import snowflake_conn

from docs.data.your.database.schema import User

with snowflake_conn.cursor() as cursor:
    delete.from_(User).where(
        "id = %s",
        [1],
    ).execute(cursor)
