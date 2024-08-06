from typing import Any, Callable

from pydantic import Field


def DefaultFactory(default_factory: Callable[[], Any]) -> Any:
    """
    The wrapper for the combination of `Annotated` and `default_factory`.

    See: https://github.com/pydantic/pydantic/issues/9769
    """
    return Field(default_factory=default_factory)
