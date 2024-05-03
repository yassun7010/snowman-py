from conftest import User
from snowman.protocol.cursor import Cursor
from snowman.query import update


class TestUpdateStatement:
    def test_update_statement(self, user: User, cursor: Cursor):
        update(User).set(user).execute(cursor)
