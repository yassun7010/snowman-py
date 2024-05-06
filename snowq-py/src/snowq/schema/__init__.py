from typing import Type, TypeVar

from pydantic import BaseModel

from snowq.schema.external_table import ExternalTable
from snowq.schema.materiarized_view import MateriarizedView
from snowq.schema.table import Table
from snowq.schema.view import View

Tablable = Table
Viewable = View | ExternalTable | MateriarizedView

GenericTablable = TypeVar("GenericTablable", bound=Tablable)


def full_name(table: Type[Tablable]) -> str:
    return f"{table.__databas_name__}.{table.__schema_name__}.{table.__table_name__}"


def field_names(table: Type[Table]) -> list[str]:
    if issubclass(table, BaseModel):
        return [field_name for field_name in table.model_fields.keys()]

    else:
        raise ValueError(f"Table {table} is not a Pydantic model")
