## Data Types

Snowman provides Python types corresponding to
[the data types supported by Snowflake](https://docs.snowflake.com/en/sql-reference-data-types),
which are defined in the `snowman.datatype` module.

!!! note
    Snowman automatically retrieves these data types from the Snowflake database,
    so you don't need to specify these types directly.

| Snowman Data Type                    | Python Type         |
|--------------------------------------|---------------------|
| `snowman.datatype.NUMBER`            | `float`             |
| `snowman.datatype.DECIMAL`           | `decimal.Decimal`   |
| `snowman.datatype.NUMERIC`           | `float`             |
| `snowman.datatype.INT`               | `int`               |
| `snowman.datatype.INTEGER`           | `int`               |
| `snowman.datatype.BIGINT`            | `int`               |
| `snowman.datatype.SMALLINT`          | `int`               |
| `snowman.datatype.TINYINT`           | `int`               |
| `snowman.datatype.BYTEINT`           | `int`               |
| `snowman.datatype.FLOAT`             | `float`             |
| `snowman.datatype.FLOAT4`            | `float`             |
| `snowman.datatype.FLOAT8`            | `float`             |
| `snowman.datatype.DOUBLE`            | `float`             |
| `snowman.datatype.REAL`              | `float`             |
| `snowman.datatype.VARCHAR`           | `str`               |
| `snowman.datatype.CHAR`              | `str`               |
| `snowman.datatype.CHARACTER`         | `str`               |
| `snowman.datatype.STRING`            | `str`               |
| `snowman.datatype.TEXT`              | `str`               |
| `snowman.datatype.BINARY`            | `bytes`             |
| `snowman.datatype.VARBINARY`         | `bytes`             |
| `snowman.datatype.BOOLEAN`           | `bool`              |
| `snowman.datatype.DATE`              | `datetime.date`     |
| `snowman.datatype.DATETIME`          | `datetime.datetime` |
| `snowman.datatype.TIME`              | `datetime.time`     |
| `snowman.datatype.TIMESTAMP`         | `datetime.datetime` |
| `snowman.datatype.TIMESTAMP_LTZ`     | `datetime.datetime` |
| `snowman.datatype.TIMESTAMP_NTZ`     | `datetime.datetime` |
| `snowman.datatype.TIMESTAMP_TZ`      | `datetime.datetime` |
| `snowman.datatype.VARIANT`           | `Any`               |
| `snowman.datatype.OBJECT`            | `dict[str, Any]`    |
| `snowman.datatype.ARRAY`             | `list[Any]`         |
| `snowman.datatype.GEOGRAPHY`         | `Any`               |
| `snowman.datatype.GEOMETRY`          | `Any`               |
