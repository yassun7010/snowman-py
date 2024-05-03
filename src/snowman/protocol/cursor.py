from snowflake.connector.cursor import SnowflakeCursor

try:
    import turu.snowflake

    TuruSnowflakeConnection = turu.snowflake.Connection
    TuruSnowflakeCursor = turu.snowflake.Cursor

except ImportError:
    TuruSnowflakeConnection = SnowflakeCursor
    TuruSnowflakeCursor = SnowflakeCursor

Cursor = SnowflakeCursor | TuruSnowflakeConnection | TuruSnowflakeCursor
