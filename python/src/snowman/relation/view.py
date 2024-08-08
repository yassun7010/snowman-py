from typing import Callable, ClassVar, Generic, LiteralString, Type, TypeVar

from pydantic import BaseModel

from snowman.relation.table import GenericColumnAccessor


class View(BaseModel, Generic[GenericColumnAccessor]):
    """
    Base class for view definition.
    """

    # NOTE: Meta information to specify the table name accurately.
    #       It is used when creating a query.
    __database_name__: ClassVar[str]
    __schema_name__: ClassVar[str]
    __table_name__: ClassVar[str]

    # NOTE: This field exists only for type definition and is not accessed at runtime.
    __access_columns__: Type[GenericColumnAccessor] | None = None


GenericView = TypeVar("GenericView", bound=View)


def view(
    database_name: LiteralString,
    schema_name: LiteralString,
    table_name: LiteralString,
    /,
) -> "Callable[[Type[GenericView]], Type[GenericView]]":
    def decorate(cls: "Type[GenericView]") -> "Type[GenericView]":
        cls.__database_name__ = database_name
        cls.__schema_name__ = schema_name
        cls.__table_name__ = table_name

        return cls

    return decorate
