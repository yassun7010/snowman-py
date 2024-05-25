from typing import Type

from snowq.query._builder._insert_query_builder import InsertQueryBuilder
from snowq.query._builder._update_query_builder import UpdateStatement
from snowq.schema.table import (
    GenericInsertColumnTypedDict,
    GenericUpdateColumnTypedDict,
    Table,
)

insert = InsertQueryBuilder()


def update(
    table: Type[Table[GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]],
):
    return UpdateStatement(
        table,
        _columns_type=table.__update_columns__,  # type: ignore
    )
