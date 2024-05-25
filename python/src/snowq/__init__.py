import importlib
import importlib.metadata

from . import datatype as datatype
from . import query as query
from .schema.table import Table as Table
from .schema.table import table as table

__version__ = importlib.metadata.version("snowq")
