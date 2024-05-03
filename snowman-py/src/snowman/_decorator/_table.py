from typing import Callable, LiteralString, Type

from snowman.schema.table import Table


def table(
    database_name: LiteralString,
    schema_name: LiteralString,
    table_name: LiteralString,
    /,
) -> Callable[[Type[Table]], Type[Table]]:
    def decorate(cls: Type[Table]) -> Type[Table]:
        return cls

    return decorate
