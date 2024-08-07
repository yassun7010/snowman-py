from typing import Generic, Type

from snowman.query.column import get_columns
from snowman.relation.table import (
    GenericAccessColumnDataclass,
    GenericInsertColumnTypedDict,
    GenericUpdateColumnTypedDict,
    Table,
)


class WhereContext(Generic[GenericAccessColumnDataclass]):
    def __call__(
        self,
        table: Type[
            Table[
                GenericAccessColumnDataclass,
                GenericInsertColumnTypedDict,
                GenericUpdateColumnTypedDict,
            ]
        ],
    ) -> GenericAccessColumnDataclass:
        return get_columns(table)
