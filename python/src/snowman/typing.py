from typing import Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class TypeMissMatch(Generic[T, U]):
    """
    Type Hint for Type Miss Match.
    """


class UseIsInsteadOfEq:
    """
    Please use `.is_` instead of `==`.
    """


class UseIsNotInsteadOfNe:
    """
    Please use `.is_.not_` instead of `!=`.
    """
