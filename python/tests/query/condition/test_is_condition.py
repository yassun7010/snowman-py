from snowman.query.column import Column


class TestIsCondition:
    def test_is_null_condition(self, int_column: Column[int]):
        condition = int_column.is_.null.to_sql()
        assert condition.condition == "id IS NULL"
        assert condition.params == ()

    def test_is_true_condition(self, int_column: Column[int]):
        condition = int_column.is_.true.to_sql()
        assert condition.condition == "id IS TRUE"
        assert condition.params == ()

    def test_is_false_condition(self, int_column: Column[int]):
        condition = int_column.is_.false.to_sql()
        assert condition.condition == "id IS FALSE"
        assert condition.params == ()
