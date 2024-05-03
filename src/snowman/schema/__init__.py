from typing import TypeVar

from snowman.schema.external_table import ExternalTable
from snowman.schema.materiarized_view import MateriarizedView
from snowman.schema.table import Table
from snowman.schema.view import View

Tablable = Table
Viewable = View | ExternalTable | MateriarizedView

GenericTablable = TypeVar("GenericTablable", bound=Tablable)
