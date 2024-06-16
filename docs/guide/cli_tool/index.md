# CLI Tool

The `snowman` command is provided to assist in the integration between Snowflake and Python.

## Initialization
### `$ snowman init`

Initialize Snowman configuration.

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

### `$ snowman model diff`

Check differences between Python models and Snowflake information schemas.

!!! example
    ```sh
    snowman model diff --check
    ```