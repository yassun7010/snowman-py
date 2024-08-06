from snowman.query.column import Column


class TestIsNotCondition:
    def test_is_not_null_condition(self, id_column: Column[int]):
        condition = id_column.is_.not_.null.to_condition()
        assert condition.condition == "id IS NOT NULL"
        assert condition.params == ()

    def test_is_not_true_condition(self, id_column: Column[int]):
        condition = id_column.is_.not_.true.to_condition()
        assert condition.condition == "id IS NOT TRUE"
        assert condition.params == ()

    def test_is_not_false_condition(self, id_column: Column[int]):
        condition = id_column.is_.not_.false.to_condition()
        assert condition.condition == "id IS NOT FALSE"
        assert condition.params == ()
