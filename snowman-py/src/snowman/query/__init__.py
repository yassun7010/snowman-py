from typing import Type

from snowman.query._builder._insert_query_builder import InsertQueryBuilder
from snowman.query._builder._update_query_builder import UpdateStatement
from snowman.schema import Tablable

insert = InsertQueryBuilder()


def update(table: Type[Tablable]) -> UpdateStatement:
    return UpdateStatement(table)
