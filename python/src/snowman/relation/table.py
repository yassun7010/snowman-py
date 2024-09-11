from typing import (
    Callable,
    ClassVar,
    Generic,
    LiteralString,
    Type,
    TypedDict,
    TypeVar,
)

from pydantic import BaseModel


class AccessColumnTypedDict(TypedDict):
    pass


class InsertColumnTypedDict(TypedDict):
    pass


class UpdateColumnTypedDict(TypedDict, total=False):
    pass


_GenericTable = TypeVar("_GenericTable")

GenericColumnAccessor = TypeVar(
    "GenericColumnAccessor",
)

GenericInsertColumnTypedDict = TypeVar(
    "GenericInsertColumnTypedDict",
    bound=InsertColumnTypedDict,
)

GenericUpdateColumnTypedDict = TypeVar(
    "GenericUpdateColumnTypedDict",
    bound=UpdateColumnTypedDict,
)


class Table(
    BaseModel,
    Generic[
        _GenericTable,
        GenericColumnAccessor,
        GenericInsertColumnTypedDict,
        GenericUpdateColumnTypedDict,
    ],
):
    """
    Base class for table definition.
    """

    # NOTE: Meta information to specify the table name accurately.
    #       It is used when creating a query.
    __database_name__: ClassVar[str]
    __schema_name__: ClassVar[str]
    __table_name__: ClassVar[str]

    # NOTE: This field exists only for type definition and is not accessed at runtime.
    __access_columns__: Type[GenericColumnAccessor] | None = None
    __insert_columns__: Type[GenericInsertColumnTypedDict] | None = None
    __update_columns__: Type[GenericUpdateColumnTypedDict] | None = None


GenericTable = TypeVar("GenericTable", bound=Table)


def table(
    database_name: LiteralString,
    schema_name: LiteralString,
    table_name: LiteralString,
    /,
) -> "Callable[[Type[GenericTable]], Type[GenericTable]]":
    def decorate(cls: "Type[GenericTable]") -> "Type[GenericTable]":
        cls.__database_name__ = database_name
        cls.__schema_name__ = schema_name
        cls.__table_name__ = table_name

        return cls

    return decorate
