from typing import Callable, ClassVar, Generic, LiteralString, Type, TypedDict, TypeVar


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


class Table(Generic[GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]):
    __databas_name__: ClassVar[str]
    __schema_name__: ClassVar[str]
    __table_name__: ClassVar[str]
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
