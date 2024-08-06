from snowman.query import truncate
from your.snowflake import snowflake_conn

from docs.data.your.database.aaaschema import User

with snowflake_conn.cursor() as cursor:
    truncate.if_.exists.table(User).execute(cursor)
