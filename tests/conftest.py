import pytest
import snowman
from snowman.protocol.cursor import Cursor
from snowman.schema.table import Table


@pytest.fixture
def cursor() -> Cursor:
    class MyCursor:
        def execute(self, *args, **kwargs) -> None:
            pass

        def executemany(self, *args, **kwargs) -> None:
            pass

    return MyCursor()


@snowman.table("database", "schema", "users")
class User(Table):
    pass


@pytest.fixture
def user() -> User:
    return User()
