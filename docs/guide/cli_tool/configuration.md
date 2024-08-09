# Configuration

This section describes how to customize the behavior of the `snowman` command.

The configuration written in `snowman.toml` or `[tool.snowman]` of `pyproject.toml` are loaded.
Instructions by command arguments have higher priority than the configuration file, and it is possible to override the configuration specified in the configuration file.

## `connection`

Set the connection information to Snowflake. Each setting item can be specified directly from the configuration file, or you can specify the environment variable name in the `env` property to get the value from the environment variable.

!!! example
    ```toml
    [connection]
    account = { env = "SNOWFLAKE_ACCOUNT" }
    user = { env = "SNOWFLAKE_USER" }
    password = { env = "SNOWFLAKE_PASSWORD" }
    role = "DEVELOPER"
    database = "MY_DB"
    schema = "PUBLIC"
    warehouse = "XSMALL"
    ```

## `model`
### `output_dir`

Specify the output directory of the Pydantic models generated from the Snowflake information schema.

!!! example
    ```toml
    [model]
    output_dir = "src/models"
    ```

### `table_types`
Specify the table types that are the target of model generation.  
The default value is `["BASE TABLE", "VIEW"]`

!!! example
    ```toml
    # Top Level
    [model]
    table_types = ["BASE TABLE"]
    
    # Database Level
    [model.database.MY_DB]
    table_types = ["BASE TABLE"]

    # Schema Level
    [model.database.MY_DB.schema.MY_SCHEMA]
    table_types = ["BASE TABLE"]
    ```


### `include_databases`
Specify the database names that are the target of model generation. It cannot be used in conjunction with `[model.exclude_databases]`.

!!! example
    ```toml
    [model]
    include_databases = ["MY_DB"]
    ```

### `exclude_datebases`
Specify the database names that are not the target of model generation. It cannot be used in conjunction with `[model.include_databases]`.

!!! example
    ```toml
    [model]
    exclude_databases = ["INFORMATION_SCHEMA", "MIGRATION"]
    ```

### `include_schemas`
Specify the schema names that are the target of model generation. It cannot be used in conjunction with `[model.database.*.exclude_schemas]`.

!!! example
    ```toml
    [model.database.MY_DB]
    include_schemas = ["PUBLIC"]
    ```

### `exclude_schemas`
Specify the schema names that are not the target of model generation. It cannot be used in conjunction with `[model.database.*.include_schemas]`.

!!! example
    ```toml
    [model.database.MY_DB]
    exclude_schemas = ["SANDBOX"]
    ```

## `pydantic`
Configure the Pydantic models to be generated.


### `model_name_prefix`
Specify the prefix of the Pydantic model name.

!!! example
    ```toml
    [pydantic]
    model_name_prefix = "Model"
    ```

    The following conversion is performed:

    `database.schema.user` -> `database.schema.ModelUser`

### `model_name_suffix`
Specify the suffix of the Pydantic model name.

!!! example
    ```toml
    [pydantic]
    model_name_suffix = "Model"
    ```

    The following conversion is performed:

    `database.schema.user` -> `database.schema.UserModel`
