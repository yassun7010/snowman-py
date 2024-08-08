import datetime
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
    .where(
        lambda c: (c(User).name.in_(["Jane", "Doe"]))
        .and_(c(User).age > 18)
        .and_(c(User).created_at >= datetime.datetime(2001, 1, 1))
    )
).build()

expected = textwrap.dedent(
    """
    UPDATE
        DATABASE.SCHEMA.USER
    SET
        name = %s
    WHERE
        name IN (%s)
        AND age > %s
        AND created_at >= %s
    """,
).strip()

assert query == expected
assert params == ("Jane Doe", ["Jane", "Doe"], 18, datetime.datetime(2001, 1, 1))
