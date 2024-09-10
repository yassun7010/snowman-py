import datetime

from snowman.query import update
from your.database.schema import User
from your.snowflake import snowflake_conn

with snowflake_conn.cursor() as cursor:
    update(
        User,
    ).set(
        {"name": "Jane Doe"},
    ).where(
        lambda c: (c(User).name.in_(["Jane", "Doe"]))
        .and_(
            c.group(
                (c(User).age.is_.not_.null)
                .and_(c(User).age >= 18)
                .and_(c(User).age <= 100),
            ),
        )
        .and_(c(User).created_at >= datetime.datetime(2001, 1, 1)),
    ).execute(cursor)
