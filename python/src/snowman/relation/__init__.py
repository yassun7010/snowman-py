from typing import Any, Type, cast

from pydantic import BaseModel

from snowman.relation.table import (
    GenericInsertColumnTypedDict,
    GenericUpdateColumnTypedDict,
    Table,
)


def full_table_name(table: Type[Table]) -> str:
    return f"{table.__databas_name__}.{table.__schema_name__}.{table.__table_name__}"


def table_column_names(table: Type[Table]) -> list[str]:
    if issubclass(table, BaseModel):
        return [column_name for column_name in table.model_fields.keys()]

    else:
        raise ValueError(f"Table {table} is not a Pydantic model")


def table_columns_dict(
    table: Table[GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]
    | GenericInsertColumnTypedDict
    | GenericUpdateColumnTypedDict,
) -> dict[str, Any]:
    if isinstance(table, BaseModel):
        return table.model_dump()

    elif isinstance(table, dict):
        return cast(dict, table)

    else:
        raise ValueError(f"Table {table} is not a Pydantic model")
