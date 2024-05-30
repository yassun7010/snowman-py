# snowq

Easily build and execute Snowflake queries in Python.


## CLI Tool

### New snowq Config
```sh
snowq new
```

### Generate Python Model from Snowflake information schema
```sh
snowq model import
```


## Query Builder

### Insert Query

```python
import textwrap

from snowq.query import insert

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

from snowq.query import update

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

from snowq.query import delete

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
from snowq.query import truncate

from your.database.schema import User

query, params = truncate.table(User).build()

expected = "TRUNCATE TABLE database.schema.users"

assert query == expected
```
