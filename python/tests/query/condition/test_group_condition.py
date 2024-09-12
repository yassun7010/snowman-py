from typing import assert_type

from conftest import User
from snowman.query.builder.condition.group_condition import GroupCondition
from snowman.query.expression import column as c


class TestGroupCondition:
    def test_group_condition(self):
        condition = GroupCondition(c(User).id == 1)
        sql = condition.to_sql()

        assert_type(condition, GroupCondition)
        assert sql.operation == "(id = %s)"
        assert sql.params == (1,)
