# CLI Tool

The `snowman` command is provided to assist in the integration between Snowflake and Python.

## Initialization
### `$ snowman init`

Initialize Snowman configuration. For more information on configuration items, please read [Configuration](./configuration.md#Configuration).

!!! tip
    Initialize the `snowman.toml` file or set `[tool.snowman]` in `pyproject.toml` with the `--file` option. By default, the `snowman.toml` file is created.

!!! example
    ```sh
    snowman init
    ```

## Python Model Generator
### `$ snowman model generate`

Automatically generate Pydantic models from Snowflake information schemas.

!!! example
    ```sh
    snowman model generate
    ```

??? note "Generated Code"
    #### SQL DDL
    ```sql
    --8<-- "docs/data/model_schema.sql"
    ```

    #### Python Code
    ```python
    --8<-- "docs/data/model_generate.py"
    ```


### `$ snowman model diff`

Check differences between Python models and Snowflake information schemas.

!!! example
    ```sh
    snowman model diff --check
    ```
