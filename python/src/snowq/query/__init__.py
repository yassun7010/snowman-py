from typing import Type

from snowq.query._builder._delete_query_builder import DeleteQueryBuilder
from snowq.query._builder._insert_query_builder import InsertQueryBuilder
from snowq.query._builder._truncate_query_builder import TruncateQueryBuilder
from snowq.query._builder._update_query_builder import UpdateStatement
from snowq.relation.table import (
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


delete = DeleteQueryBuilder()

truncate = TruncateQueryBuilder()


__all__ = [
    "insert",
    "update",
    "delete",
    "truncate",
]
