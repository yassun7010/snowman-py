import pytest
from snowman.protocol.connection import Connection


@pytest.fixture
def connection() -> Connection:
    class MyConnection:
        def execute(self, *args, **kwargs) -> None:
            pass

        def executemany(self, *args, **kwargs) -> None:
            pass

    return MyConnection()
