from textwrap import dedent
from typing import Generic, Sequence, Type

from typing_extensions import override

from snowq.schema import GenericTablable, field_names, full_name

from ._builder import QueryBuilder, QueryParams


class InsertQueryBuilder:
    @property
    def overwrite(self) -> "InsertOverwriteQueryBuilder":
        return InsertOverwriteQueryBuilder()

    def into(self, table: Type[GenericTablable]) -> "InsertIntoQueryBuilder":
        return InsertIntoQueryBuilder(table)


class InsertOverwriteQueryBuilder:
    def into(self, table: Type[GenericTablable]) -> "InsertIntoQueryBuilder":
        return InsertIntoQueryBuilder(table, overwtire=True)


class InsertIntoQueryBuilder(Generic[GenericTablable]):
    def __init__(
        self,
        table: Type[GenericTablable],
        overwtire: bool = False,
    ) -> None:
        self._table = table
        self._overwrite = overwtire

    def values(
        self, value: GenericTablable, *values: GenericTablable
    ) -> "InsertIntoValuesQueryBuilder":
        return InsertIntoValuesQueryBuilder(
            self._table,
            (value, values),
            overwrite=self._overwrite,
        )


class InsertIntoValuesQueryBuilder(Generic[GenericTablable], QueryBuilder):
    def __init__(
        self,
        table: type[GenericTablable],
        values: Sequence[GenericTablable],
        /,
        overwrite: bool = False,
    ):
        self._table = table
        self._values = values
        self._overwrite = overwrite

    @override
    def build(self) -> QueryParams:
        overwrite = "OVERWRITE " if self._overwrite else ""
        query = dedent(
            f"""
            INSERT {overwrite}INTO
                {full_name(self._table)}
            VALUES (
                {", ".join(['?' for value in field_names(self._table)])}
            )
            """
        ).strip()

        return QueryParams(query, {})
