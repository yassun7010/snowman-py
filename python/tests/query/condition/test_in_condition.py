from typing import assert_type

import pytest
from conftest import User
from snowman.query.builder.condition.in_condition import InCondition
from snowman.query.expression import column as c


class TestInCondition:
    def test_in_condition(self):
        condition = c(User).id.in_([1, 2])
        sql = condition.to_sql()

        assert_type(condition, InCondition)
        assert sql.operation == "id IN (%s)"
        assert sql.params == ([1, 2],)

    @pytest.mark.parametrize("value", [1, None])
    def test_in_condition_use_nullable(self, value: int | None):
        # NOTE: Consider whether null safety can be supported
        assert_type(c(User).age.in_([value]), InCondition)
