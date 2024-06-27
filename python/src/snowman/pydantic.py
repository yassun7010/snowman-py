from typing import Any, Callable

from pydantic import Field


# The wrapper for cohabitation of Annotated and default_factory.
#
# See: https://github.com/pydantic/pydantic/issues/9769
def DefaultFactory(default_factory: Callable[[], Any]) -> Any:
    return Field(default_factory=default_factory)
