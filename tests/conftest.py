import pytest
from snowman.protocol.cursor import Cursor


@pytest.fixture
def Cursor() -> Cursor:
    class MyCursor:
        def execute(self, *args, **kwargs) -> None:
            pass

        def executemany(self, *args, **kwargs) -> None:
            pass

    return MyCursor()
