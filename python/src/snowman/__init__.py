import importlib
import importlib.metadata

from . import datatype as datatype
from . import query as query
from .query.column import Column as Column
from .relation.table import PydanticTable as PydanticTable
from .relation.table import Table as Table
from .relation.table import table as table

__version__ = importlib.metadata.version("snowman-py")
