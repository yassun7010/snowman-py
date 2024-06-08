import pytest
from snowman.query.column import _Column


@pytest.fixture
def id_column() -> _Column[int]:
    return _Column(
        int,
        database_name="database",
        schema_name="schema",
        table_name="table",
        column_name="id",
    )


class TestIsCondition:
    def test_is_condition(self, id_column: _Column[int]):
        params = []
        assert (
            id_column.is_(None).to_condition(params)
            == "database.schema.table.id IS NULL"
        )
        assert params == []

    def test_is_not_condition(self, id_column: _Column[int]):
        params = []
        assert (
            id_column.is_.not_(None).to_condition(params)
            == "database.schema.table.id IS NOT NULL"
        )
        assert params == []
