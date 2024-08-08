import textwrap

from snowman.query import delete
from your.database.schema import User

query, params = (
    delete.from_(
        User,
    ).where(
        lambda c: c(User).id == 1,
    )
).build()

expected = textwrap.dedent(
    """
    DELETE FROM
        DATABASE.SCHEMA.USER
    WHERE
        ID = %s
    """,
).strip()

assert query == expected
assert params == (1,)
