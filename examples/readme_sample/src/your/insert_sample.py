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
