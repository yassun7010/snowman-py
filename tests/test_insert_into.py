import snowman
from conftest import User
from snowman.protocol.cursor import Cursor


class TestInsertInto:
    def test_insert_into_statement(self, user: User, cursor: Cursor):
        snowman.query.insert_into(User).values(user, user).execute(cursor)
