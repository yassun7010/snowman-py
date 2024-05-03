from typing import TypeVar

from snowq.schema.external_table import ExternalTable
from snowq.schema.materiarized_view import MateriarizedView
from snowq.schema.table import Table
from snowq.schema.view import View

Tablable = Table
Viewable = View | ExternalTable | MateriarizedView

GenericTablable = TypeVar("GenericTablable", bound=Tablable)
