import importlib
import importlib.metadata

from . import query as query
from ._decorator._table import table as table

__version__ = importlib.metadata.version("snowman-py")
