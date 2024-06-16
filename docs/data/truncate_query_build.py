from snowman.query import truncate
from your.database.schema import User

query, params = truncate.if_.exists.table(User).build()

expected = "TRUNCATE IF EXISTS TABLE database.schema.users"

assert query == expected
assert params == ()
