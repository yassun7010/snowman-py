import textwrap

from snowman import column as c
from snowman.query import delete
from your.database.schema import User

query, params = (
    delete.from_(
        User,
    ).where(
        c(User).id == 1,
    )
).build()

expected = textwrap.dedent(
    """
    DELETE FROM
        DATABASE.SCHEMA.USER
    WHERE
        id = %s
    """,
).strip()

assert query == expected
assert params == (1,)
