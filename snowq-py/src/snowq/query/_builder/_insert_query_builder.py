from textwrap import dedent
from typing import Generic, Sequence, Type

from typing_extensions import override

from snowq.schema import GenericTablable

from ._builder import QueryBuilder, QueryParams


class InsertQueryBuilder:
    @property
    def overwrite(self) -> "InsertOverwriteQueryBuilder":
        return InsertOverwriteQueryBuilder()

    def into(self, table: Type[GenericTablable]) -> "InsertIntoQueryBuilder":
        return InsertIntoQueryBuilder(table)


class InsertOverwriteQueryBuilder:
    def into(self, table: Type[GenericTablable]) -> "InsertIntoQueryBuilder":
        return InsertIntoQueryBuilder(table)


class InsertIntoQueryBuilder(Generic[GenericTablable]):
    def __init__(self, table: Type[GenericTablable], overwtire: bool = False) -> None:
        self._table = table

    def values(
        self, record: GenericTablable, *records: GenericTablable
    ) -> "InsertIntoValuesQueryBuilder":
        return InsertIntoValuesQueryBuilder(self._table, (record, *records))


class InsertIntoValuesQueryBuilder(Generic[GenericTablable], QueryBuilder):
    def __init__(self, table: type[GenericTablable], values: Sequence[GenericTablable]):
        self._table = table
        self._values = values

    @override
    def build(self) -> QueryParams:
        query = dedent(
            f"""
            INSERT INTO
                {self._table}
            VALUES (
                {", ".join(['?' for value in self._values])}
            )
            """
        ).strip()

        return QueryParams(query, {})
