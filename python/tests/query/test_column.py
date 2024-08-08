from conftest import User
from snowman.query.expression import column as c


def test_column_repr(user: User):
    assert repr(c(User).id) == "database.schema.users.id"
