from typing import Any, Type, TypeVar

from pydantic import BaseModel

from snowq.schema.external_table import ExternalTable
from snowq.schema.materiarized_view import MateriarizedView
from snowq.schema.table import GenericUpdateColumns, Table
from snowq.schema.view import View

Tablable = Table[GenericUpdateColumns]
Viewable = View | ExternalTable | MateriarizedView

GenericTablable = TypeVar("GenericTablable", bound=Tablable)


def full_name(table: Type[Tablable]) -> str:
    return f"{table.__databas_name__}.{table.__schema_name__}.{table.__table_name__}"


def column_names(table: Type[Table]) -> list[str]:
    if issubclass(table, BaseModel):
        return [column_name for column_name in table.model_fields.keys()]

    else:
        raise ValueError(f"Table {table} is not a Pydantic model")


def columns_dict(table: Table) -> dict[str, Any]:
    if isinstance(table, BaseModel):
        return table.model_dump()

    else:
        raise ValueError(f"Table {table} is not a Pydantic model")
