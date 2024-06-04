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
