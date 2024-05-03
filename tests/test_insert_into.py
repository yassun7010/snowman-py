from snowman import table
from snowman.protocol.connection import Connection
from snowman.query import insert_into
from snowman.schema.table import Table


class TestInsertInto:
    def test_insert_into_statement(self, connection: Connection):
        @table("database", "schema", "user")
        class User(Table):
            pass

        user = User()

        insert_into(User).values(user, user).execute(connection)
