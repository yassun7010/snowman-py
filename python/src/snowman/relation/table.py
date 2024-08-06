from typing import (
    TYPE_CHECKING,
    Callable,
    ClassVar,
    Generic,
    LiteralString,
    Type,
    TypedDict,
    TypeVar,
)

from pydantic._internal._model_construction import (
    ModelMetaclass as PydanticModelMetaclass,
)

if TYPE_CHECKING:
    from snowman.query.column import Column


class InsertColumnTypedDict(TypedDict):
    pass


class UpdateColumnTypedDict(TypedDict, total=False):
    pass


GenericInsertColumnTypedDict = TypeVar(
    "GenericInsertColumnTypedDict",
    bound=InsertColumnTypedDict,
)

GenericUpdateColumnTypedDict = TypeVar(
    "GenericUpdateColumnTypedDict",
    bound=UpdateColumnTypedDict,
)


class _TableMetaclass(PydanticModelMetaclass):
    __database_name__: ClassVar[str | None]
    __schema_name__: ClassVar[str | None]
    __table_name__: ClassVar[str]

    def __getattr__(cls, key: str):
        """
        Implementation to return an SQLType instance
        when the field type is accessed as a class property
        rather than an instance property.
        """

        if cls is None:
            return Column(
                str,
                database_name="TEST_DATABASE",
                schema_name="TEST_SCHEMA",
                table_name="TEST_TABLE",
                column_name=key,
            )

        else:
            return super().__getattr__(key)  # type: ignore


class Table(
    Generic[GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict],
):
    """
    Base class for table definition.
    """

    # NOTE: Meta information to specify the table name accurately.
    #       It is used when creating a query.
    __databas_name__: ClassVar[str]
    __schema_name__: ClassVar[str]
    __table_name__: ClassVar[str]

    # NOTE: This field exists only for type definition and is not accessed at runtime.
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
        cls.__databas_name__ = database_name
        cls.__schema_name__ = schema_name
        cls.__table_name__ = table_name

        return cls

    return decorate
