from snowman.query import truncate

from docs.data.your.database.aaaschema import User

query, params = truncate.if_.exists.table(User).build()

expected = "TRUNCATE IF EXISTS TABLE database.schema.users"

assert query == expected
assert params == ()
