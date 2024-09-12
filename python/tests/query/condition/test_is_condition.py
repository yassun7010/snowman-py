from conftest import User
from snowman.query.expression import column as c


class TestIsCondition:
    def test_is_null_condition(self):
        condition = c(User).id.is_.null.to_sql()
        assert condition.operation == "id IS NULL"
        assert condition.params == ()
