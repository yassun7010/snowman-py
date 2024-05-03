from snowman.protocol.cursor import Cursor
from snowman.query import update
from snowman.schema.table import Table


class TestUpdateStatement:
    def test_update_statement(self, Cursor: Cursor):
        class User(Table):
            pass

        user = User()

        update(User).set(user).execute(Cursor)
