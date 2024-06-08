"""
# [Snowman](https://github.com/yassun7010/snowman-py)

Python model and query builder for [Snowflake](https://www.snowflake.com/).
"""

import importlib
import importlib.metadata

from . import datatype as datatype
from . import query as query
from .relation.table import Table as Table
from .relation.table import table as table

__version__ = importlib.metadata.version("snowman-py")
