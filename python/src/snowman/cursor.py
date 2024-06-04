from snowflake.connector import SnowflakeConnection
from snowflake.connector.cursor import SnowflakeCursor

from snowman._features import TuruSnowflakeCursor

Cursor = SnowflakeCursor | TuruSnowflakeCursor


def _get_snowfalke_cursor(cursor: Cursor) -> SnowflakeCursor:
    if raw_cursor := getattr(cursor, "_raw_cursor", None):
        return raw_cursor

    else:
        return cursor  # type: ignore


def _get_snowflake_connection(
    cursor: Cursor,
) -> SnowflakeConnection:
    cursor = _get_snowfalke_cursor(cursor)
    return getattr(cursor, "connection")
