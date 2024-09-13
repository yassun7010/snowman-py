from typing import TypeVar

from snowman.relation.table import Table
from snowman.relation.view import View

TableLike = Table | View

GenericTableLike = TypeVar("GenericTableLike", bound=TableLike)
