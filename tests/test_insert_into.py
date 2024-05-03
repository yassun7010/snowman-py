from conftest import User
from snowman.protocol.cursor import Cursor
from snowman.query import insert_into


class TestInsertInto:
    def test_insert_into_statement(self, user: User, cursor: Cursor):
        insert_into(User).values(user, user).execute(cursor)
