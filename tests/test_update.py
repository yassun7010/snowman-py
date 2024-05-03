from snowman.protocol.connection import Connection
from snowman.query import update
from snowman.schema.table import Table


class TestUpdateStatement:
    def test_update_statement(self, connection: Connection):
        class User(Table):
            pass

        user = User()

        update(User).set(user).execute(connection)
