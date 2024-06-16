# Query Builder

Snowman provides a query builder that maintains the syntax of SQL.
You can generate `INSERT` / `UPDATE` / `DELETE` / `TRUNCATE` queries, but
it does not currently support complex query syntax like `SELECT`.

!!! tip
    The query builder is based on simple rules.

    * SQL reserved words can be written in a way that can be accessed like properties with a dot `.`
    * If a SQL reserved word matches a Python reserved word, an underscore `_` is added to the end of the property name

!!! note
    The [paramstyle](https://peps.python.org/pep-0249/#paramstyle) used by Snowman is `format`.
    The reason for not supporting `pyformat` is to avoid key duplication
    when complex query patterns occur.

## Insert Query

=== "Execute"
    !!! example
        ```python
        --8<-- "docs/data/insert_query.py"
        ```

=== "Build"
    !!! example
        ```python
        --8<-- "docs/data/insert_query_build.py"
        ```

## Update Query

=== "Execute"
    !!! example
        ```python
        --8<-- "docs/data/update_query.py"
        ```

=== "Build"
    !!! example
        ```python
        --8<-- "docs/data/update_query_build.py"
        ```

## Delete Query

=== "Execute"
    !!! example
        ```python
        --8<-- "docs/data/delete_query.py"
        ```

=== "Build"
    !!! example
        ```python
        --8<-- "docs/data/delete_query_build.py"
        ```

## Truncate Query

=== "Execute"
    !!! example
        ```python
        --8<-- "docs/data/truncate_query.py"
        ```

=== "Build"
    !!! example
        ```python
        --8<-- "docs/data/truncate_query_build.py"
        ```
