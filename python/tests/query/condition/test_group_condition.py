from typing import assert_type

from snowman.query.builder.condition.group_condition import GroupCondition
from snowman.query.column import Column


class TestGroupCondition:
    def test_group_condition(self, int_column: Column[int]):
        condition = GroupCondition(int_column == 1)
        sql = condition.to_sql()

        assert_type(condition, GroupCondition)
        assert sql.condition == "(id = %s)"
        assert sql.params == (1,)
