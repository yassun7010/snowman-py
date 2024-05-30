import textwrap

from snowq.query import update

from your.database.schema import User

query, params = (
    update(
        User,
    )
    .set({"name": "Jane Doe"})
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
