from typing import Any, Protocol


class Connection(Protocol):
    def execute(self, *args, **kwargs) -> Any: ...

    def executemany(self, *args, **kwargs) -> Any: ...
