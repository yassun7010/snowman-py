from snowman.query.column import Column


class TestIsCondition:
    def test_is_null_condition(self, int_column: Column[int]):
        condition = int_column.is_.null.to_sql()
        assert condition.condition == "id IS NULL"
        assert condition.params == ()
