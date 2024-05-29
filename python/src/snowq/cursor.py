from snowflake.connector.cursor import SnowflakeCursor

try:
    import turu.snowflake

    TuruSnowflakeCursor = turu.snowflake.Cursor

except ImportError:
    TuruSnowflakeCursor = SnowflakeCursor

Cursor = SnowflakeCursor | TuruSnowflakeCursor


def _get_snowfalke_cursor(cursor: Cursor) -> SnowflakeCursor:
    if raw_cursor := getattr(cursor, "_raw_cursor", None):
        return raw_cursor

    else:
        return cursor  # type: ignore
