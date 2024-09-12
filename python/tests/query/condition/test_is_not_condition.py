from conftest import User
from snowman.query.expression import column as c


class TestIsNotCondition:
    def test_is_not_null_condition(self):
        condition = c(User).id.is_.not_.null.to_sql()
        assert condition.operation == "id IS NOT NULL"
        assert condition.params == ()
