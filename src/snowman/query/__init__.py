from typing import Type

from snowman.query._builder._insert_into_query_builder import InsertIntoQueryBuilder
from snowman.query._builder._update_query_builder import UpdateStatement
from snowman.schema import Tablable


def insert_into(table: Type[Tablable]) -> InsertIntoQueryBuilder:
    return InsertIntoQueryBuilder(table)


def update(table: Type[Tablable]) -> UpdateStatement:
    return UpdateStatement(table)
