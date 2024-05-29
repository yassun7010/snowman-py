import importlib
import importlib.metadata

from . import datatype as datatype
from . import query as query
from .relation.table import Table as Table
from .relation.table import table as table

__version__ = importlib.metadata.version("snowq")
