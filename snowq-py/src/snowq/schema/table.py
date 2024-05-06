from typing import ClassVar, TypeVar

from typing import Callable, LiteralString, Type


class Table:
    __databas_name__: ClassVar[str]
    __schema_name__: ClassVar[str]
    __table_name__: ClassVar[str]


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
