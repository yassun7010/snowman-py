from typing import Type

from snowq.query._builder._insert_query_builder import InsertQueryBuilder
from snowq.query._builder._update_query_builder import UpdateStatement
from snowq.schema.table import GenericUpdateColumnTypedDict, Table

insert = InsertQueryBuilder()


def update(table: Type[Table[GenericUpdateColumnTypedDict]]):
    return UpdateStatement(
        table,
        table.__update_columns__,  # type: ignore
    )
