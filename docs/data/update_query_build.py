import datetime
import textwrap

from snowman import column as c
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
        (c(User).name.in_(["Jane", "Doe"]))
        .and_(c(User).age > 18)
        .and_(c(User).created_at >= datetime.datetime(2001, 1, 1))
    )
).build()

expected = textwrap.dedent(
    """
    UPDATE
        DATABASE.SCHEMA.USER
    SET
        NAME = %s
    WHERE
        NAME IN (%s)
        AND AGE > %s
        AND CREATED_AT >= %s
    """,
).strip()

assert query == expected
assert params == ("Jane Doe", ["Jane", "Doe"], 18, datetime.datetime(2001, 1, 1))
