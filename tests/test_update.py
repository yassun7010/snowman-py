import snowman
from conftest import User
from snowman.protocol.cursor import Cursor


class TestUpdateStatement:
    def test_update_statement(self, user: User, cursor: Cursor):
        snowman.query.update(User).set(user).execute(cursor)
