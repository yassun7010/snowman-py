# Query Builder

Snowman provides a query builder that maintains the syntax of SQL.
You can generate `INSERT` / `UPDATE` / `DELETE` / `TRUNCATE` queries, but
it does not currently support complex query syntax like `SELECT`.

!!! tip
    The query builder is based on simple rules.

    * SQL reserved words can be written in a way that can be accessed like properties with a dot `.`
    * If a SQL reserved word matches a Python reserved word, an underscore `_` is added to the end of the property name

    If you know `SQL`, you can build Snowman queries with a fluent python coding !! 🚀

!!! note
    The [paramstyle](https://peps.python.org/pep-0249/#paramstyle) used by Snowman is `format`.
    The reason for not supporting `pyformat` is to avoid key duplication
    when complex query patterns occur.

    In other words, it uses `%s` to embed parameters, not `%(name)s`.

## Builder Examples
### Insert Query

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

=== "Execute Many"
    !!! example
        ```python
        --8<-- "docs/data/insert_query_executemany.py"
        ```

### Update Query

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

### Delete Query

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

### Truncate Query

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

## Where Clause

There are several ways to generate the `WHERE` clause.
For simple conditions, you can complete everything in Python, and benefit from static analysis.

=== "Function"
    The method of generating the `WHERE` clause using `function` like `lambda` is the easiest way to write **type safe** queries without importing other modules.

    !!! example
        ```python
        --8<-- "docs/data/where_clause_lambda_function.py"
        ```

=== "Condition"
    The method using lambda expressions is easy to write expressions,
    but if you write complex conditions, errors may be difficult to read.  
    By using `Condition`, you can write conditions more strictly and make it easier to track errors.

    !!! example
        ```python
        --8<-- "docs/data/where_clause_condition.py"
        ```

=== "String"
    If you want to write a more complex condition, you can use string and params.  
    This method is useful when you want to write a condition that is difficult to write with `Condition`.

    !!! example
        ```python
        --8<-- "docs/data/where_clause_string.py"
        ```
