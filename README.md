# Snowman

<!-- --8<-- [start:badges] -->
[![pypi package](https://badge.fury.io/py/snowman-py.svg)](https://pypi.org/project/snowman-py)
[![python-test](https://github.com/yassun7010/snowman-py/actions/workflows/ci_python.yml/badge.svg)](https://github.com/yassun7010/snowman-py/actions)
[![rust-test](https://github.com/yassun7010/snowman-py/actions/workflows/ci_rust.yml/badge.svg)](https://github.com/yassun7010/snowman-py/actions)
<!-- --8<-- [end:badges] -->

<p align="center">
    <img alt="logo" src="https://raw.githubusercontent.com/yassun7010/snowman-py/main/docs/images/logo.svg" width="300" />
</p>


Python model and query builder for [Snowflake](https://www.snowflake.com/).

## Install

```sh
pip install snowman-py
```

## CLI Tool

### Initialize Snowman Configuration
```sh
snowman init
```

### Generate Python Model From Snowflake Information Schemas
```sh
snowman model generate
```

### Check Differences Between Python Model and Snowflake Information Schemas
```sh
snowman model diff --check
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
    (
        id,
        name
    )
    VALUES (
        %s,
        %s
    )
    """
).strip()

assert query == expected
assert params == (1, "John Doe")
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
    .where("id = %s", [1])
).build()

expected = textwrap.dedent(
    """
    UPDATE
        database.schema.users
    SET
        name = %s
    WHERE
        id = %s
    """
).strip()

assert query == expected
assert params == ("Jane Doe", 1)
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
        "id = %s",
        [1],
    )
).build()

expected = textwrap.dedent(
    """
    DELETE FROM
        database.schema.users
    WHERE
        id = %s
    """
).strip()

assert query == expected
assert params == (1,)
```

### Truncate Query

```python
from snowman.query import truncate

from your.database.schema import User

query, params = truncate.table(User).build()

expected = "TRUNCATE TABLE database.schema.users"

assert query == expected
assert params == ()
```
