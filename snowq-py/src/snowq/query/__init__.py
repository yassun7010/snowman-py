from typing import Type

from snowq.query._builder._insert_query_builder import InsertQueryBuilder
from snowq.query._builder._update_query_builder import UpdateStatement
from snowq.schema import Tablable

insert = InsertQueryBuilder()


def update(table: Type[Tablable]) -> UpdateStatement:
    return UpdateStatement(table)
