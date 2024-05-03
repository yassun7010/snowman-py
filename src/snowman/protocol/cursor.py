from typing import Any, Protocol


class Cursor(Protocol):
    """
    Cursor protocol.

    This implements the minimum required interface for snowman.

    Reference: [PEP 249 – Python Database API Specification v2.0](https://peps.python.org/pep-0249/#id20)
    """

    def execute(self, *args, **kwargs) -> Any: ...

    def executemany(self, *args, **kwargs) -> Any: ...
