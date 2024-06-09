"""
Snowman provides simple query builder for `insert` / `update` / `delete` / `truncate`.
"""

from typing import Type

from snowman.query._builder._delete_query_builder import DeleteQueryBuilder
from snowman.query._builder._insert_query_builder import InsertQueryBuilder
from snowman.query._builder._truncate_query_builder import TruncateQueryBuilder
from snowman.query._builder._update_query_builder import UpdateStatement
from snowman.relation.table import (
    GenericInsertColumnTypedDict,
    GenericUpdateColumnTypedDict,
    Table,
)

insert = InsertQueryBuilder()
"""
Insert query builder.
"""


def update(
    table: Type[Table[GenericInsertColumnTypedDict, GenericUpdateColumnTypedDict]],
):
    """
    Update query builder.
    """
    return UpdateStatement(
        table,
        _columns_type=table.__update_columns__,  # type: ignore
    )


delete = DeleteQueryBuilder()
"""
Delete query builder.
"""

truncate = TruncateQueryBuilder()
"""
Truncate query builder.
"""
