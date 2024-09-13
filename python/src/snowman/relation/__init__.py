from typing import Any, Type, cast

from pydantic import BaseModel

from snowman.relation.table import (
    GenericColumnAccessor,
    GenericInsertColumnTypedDict,
    GenericOrderItemAccessor,
    GenericTable,
    GenericUpdateColumnTypedDict,
    Table,
)
from snowman.relation.table_like import TableLike


def full_table_name(table: Type[TableLike]) -> str:
    return f"{table.__database_name__}.{table.__schema_name__}.{table.__table_name__}"


def table_column_names(table: Type[TableLike]) -> list[str]:
    if issubclass(table, BaseModel):
        return [
            field.alias if field.alias else name
            for name, field in table.model_fields.items()
        ]

    else:
        raise ValueError(f"Table {table} is not a Pydantic model")


def table_columns_dict(
    table: Table[
        GenericTable,
        GenericColumnAccessor,
        GenericOrderItemAccessor,
        GenericInsertColumnTypedDict,
        GenericUpdateColumnTypedDict,
    ]
    | GenericInsertColumnTypedDict
    | GenericUpdateColumnTypedDict,
) -> dict[str, Any]:
    if isinstance(table, BaseModel):
        return table.model_dump()

    elif isinstance(table, dict):
        return cast(dict, table)

    else:
        raise ValueError(f"Table {table} is not a Pydantic model")
