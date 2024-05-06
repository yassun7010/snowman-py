from typing import ClassVar, Generic, TypeVar, TypedDict

from typing import Callable, LiteralString, Type


class UpdateColumns(TypedDict, total=False):
    pass


GenericUpdateColumns = TypeVar("GenericUpdateColumns", bound=UpdateColumns)


class Table(Generic[GenericUpdateColumns]):
    __databas_name__: ClassVar[str]
    __schema_name__: ClassVar[str]
    __table_name__: ClassVar[str]
    __update_columns__: GenericUpdateColumns | None = None


GenericTableModel = TypeVar("GenericTableModel", bound=Table)


def table(
    database_name: LiteralString,
    schema_name: LiteralString,
    table_name: LiteralString,
    /,
) -> "Callable[[Type[GenericTableModel]], Type[GenericTableModel]]":
    def decorate(cls: "Type[GenericTableModel]") -> "Type[GenericTableModel]":
        cls.__databas_name__ = database_name
        cls.__schema_name__ = schema_name
        cls.__table_name__ = table_name

        return cls

    return decorate
