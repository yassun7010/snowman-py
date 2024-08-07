from typing import Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class TypeMissMatch(Generic[T, U]):
    """
    Type Hint for Type Miss Match.
    """
