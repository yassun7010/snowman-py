# snowman

<!-- --8<-- [start:badges] -->
[![pypi package](https://badge.fury.io/py/snowman.svg)](https://pypi.org/project/snowman)
[![python-test](https://github.com/yassun7010/snowman/actions/workflows/ci_python.yml/badge.svg)](https://github.com/yassun7010/snowman/actions)
[![rust-test](https://github.com/yassun7010/snowman/actions/workflows/ci_rust.yml/badge.svg)](https://github.com/yassun7010/snowman/actions)
<!-- --8<-- [end:badges] -->

<p align="center">
    <img alt="logo" src="https://raw.githubusercontent.com/yassun7010/snowman/main/images/logo.svg" width="300" />
</p>


A tool to easily generate Pydantic models of Snowflake tables in Python.

## CLI Tool

### Create snowman Config
```sh
snowman config create
```

### Generate Python Model From Snowflake Information Schema
```sh
snowman model generate
```


## Query Builder

### Insert Query

```python
import textwrap

from snowman.query import insert

from your.database.schema import User

query, params = (
    insert.into(
        User,
    ).values(
        {
            "id": 1,
            "name": "John Doe",
        }
    )
).build()

expected = textwrap.dedent(
    """
    INSERT INTO
        database.schema.users
    VALUES (
        %(id)s,
        %(name)s
    )
    """
).strip()

assert query == expected
```

### Update Query

```python
import textwrap

from snowman.query import update

from your.database.schema import User

query, params = (
    update(
        User,
    )
    .set(
        {"name": "Jane Doe"},
    )
    .where(
        "id = 1",
    )
).build()

expected = textwrap.dedent(
    """
    UPDATE
        database.schema.users
    SET
        name = %(name)s
    WHERE
        id = 1
    """
).strip()

assert query == expected
```

### Delete Query

```python
import textwrap

from snowman.query import delete

from your.database.schema import User

query, params = (
    delete.from_(
        User,
    ).where(
        "id = 1",
    )
).build()

expected = textwrap.dedent(
    """
    DELETE FROM
        database.schema.users
    WHERE
        id = 1
    """
).strip()

assert query == expected
```

### Truncate Query

```python
from snowman.query import truncate

from your.database.schema import User

query, params = truncate.table(User).build()

expected = "TRUNCATE TABLE database.schema.users"

assert query == expected
```
