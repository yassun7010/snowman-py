from snowman.query.column import Column


class TestIsCondition:
    def test_is_null_condition(self, id_column: Column[int]):
        condition = id_column.is_.null.to_condition()
        assert condition.condition == "database.schema.table.id IS NULL"
        assert condition.params == ()

    def test_is_true_condition(self, id_column: Column[int]):
        condition = id_column.is_.true.to_condition()
        assert condition.condition == "database.schema.table.id IS TRUE"
        assert condition.params == ()

    def test_is_false_condition(self, id_column: Column[int]):
        condition = id_column.is_.false.to_condition()
        assert condition.condition == "database.schema.table.id IS FALSE"
        assert condition.params == ()
