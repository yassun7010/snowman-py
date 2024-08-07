import datetime
import textwrap

from snowman.query import insert
from your.database.schema import User

now = datetime.datetime.now()

query, params = (
    insert.into(
        User,
    ).values(
        User(
            id=1,
            name="John Doe",
            created_at=now,
        ),
    )
).build()

expected = textwrap.dedent(
    """
    INSERT INTO
        DATABASE.SCHEMA.USER
    (
        id,
        name,
        age,
        created_at
    )
    VALUES (
        %s,
        %s,
        %s,
        %s
    )
    """,
).strip()

assert query == expected
assert params == (1, "John Doe", None, now)
