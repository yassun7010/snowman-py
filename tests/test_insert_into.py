import snowman
from snowman.protocol.cursor import Cursor
from snowman.query import insert_into
from snowman.schema.table import Table


class TestInsertInto:
    def test_insert_into_statement(self, Cursor: Cursor):
        @snowman.table("database", "schema", "user")
        class User(Table):
            pass

        user = User()

        insert_into(User).values(user, user).execute(Cursor)
