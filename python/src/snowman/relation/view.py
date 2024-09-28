from typing import Callable, ClassVar, Generic, LiteralString, Type, TypeVar

import pydantic

from snowman.relation.table import GenericColumnAccessor, GenericOrderItemAccessor


class View(
    pydantic.BaseModel, Generic[GenericColumnAccessor, GenericOrderItemAccessor]
):
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

    model_config = pydantic.ConfigDict(populate_by_name=True)


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
