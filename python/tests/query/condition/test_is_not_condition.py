from snowman.query.column import Column


class TestIsNotNullCondition:
    def test_is_not_null_condition(self, int_column: Column[int]):
        condition = int_column.is_not_null.to_sql()
        assert condition.condition == "id IS NOT NULL"
        assert condition.params == ()
