import textwrap

from snowman.query import insert
from your.database.schema import User

query, params = (
    insert.into(
        User,
    ).values(
        User(
            id=1,
            name="John Doe",
        ),
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
    """,
).strip()

assert query == expected
assert params == (1, "John Doe")
