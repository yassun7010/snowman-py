from typing import Generic, Sequence, Type

from typing_extensions import override

from snowq.schema import GenericTable, column_names, columns_dict, full_name

from ._builder import QueryBuilder, QueryParams


class InsertQueryBuilder:
    @property
    def overwrite(self) -> "InsertOverwriteQueryBuilder":
        return InsertOverwriteQueryBuilder()

    def into(self, table: Type[GenericTable]) -> "InsertIntoQueryBuilder[GenericTable]":
        return InsertIntoQueryBuilder(table)


class InsertOverwriteQueryBuilder:
    def into(self, table: Type[GenericTable]) -> "InsertIntoQueryBuilder":
        return InsertIntoQueryBuilder(table, overwtire=True)


class InsertIntoQueryBuilder(Generic[GenericTable]):
    def __init__(
        self,
        table: Type[GenericTable],
        overwtire: bool = False,
    ) -> None:
        self._table = table
        self._overwrite = overwtire

    def values(
        self, values: GenericTable | Sequence[GenericTable]
    ) -> "InsertIntoValuesQueryBuilder[GenericTable]":
        return InsertIntoValuesQueryBuilder(
            self._table,
            values if isinstance(values, Sequence) else (values,),
            overwrite=self._overwrite,
        )


class InsertIntoValuesQueryBuilder(Generic[GenericTable], QueryBuilder):
    def __init__(
        self,
        table: type[GenericTable],
        values: Sequence[GenericTable],
        /,
        overwrite: bool = False,
    ):
        self._table = table
        self._values = values
        self._overwrite = overwrite

    @override
    def build(self) -> QueryParams:
        overwrite = "OVERWRITE " if self._overwrite else ""
        query = f"""
INSERT {overwrite}INTO
    {full_name(self._table)}
VALUES (
    {',\n    '.join([f'%({column_name})s' for column_name in column_names(self._table)])}
)
""".strip()

        return QueryParams(
            query,
            columns_dict(self._values[0])
            if len(self._values) == 1
            else tuple(columns_dict(value) for value in self._values),
        )
