import importlib
import importlib.metadata

from . import query as query
from .schema.table import table as table

__version__ = importlib.metadata.version("snowq")
