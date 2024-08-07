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
    .where(lambda c: c(User).id == 1)
).build()

expected = textwrap.dedent(
    """
    UPDATE
        DATABASE.SCHEMA.USER
    SET
        name = %s
    WHERE
        id = %s
    """,
).strip()

assert query == expected
assert params == ("Jane Doe", 1)
