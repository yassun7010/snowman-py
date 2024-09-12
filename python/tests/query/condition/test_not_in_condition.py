from typing import assert_type

import pytest
from conftest import User
from snowman.query.builder.condition.not_in_condition import NotInCondition
from snowman.query.expression import column as c


class TestNotInCondition:
    def test_not_in_condition(self):
        condition = c(User).id.not_.in_([1, 2])
        sql = condition.to_sql()

        assert_type(condition, NotInCondition)
        assert sql.operation == "id NOT IN (%s)"
        assert sql.params == ([1, 2],)

    @pytest.mark.parametrize("value", [1, None])
    def test_not_in_condition_use_nullable(self, value: int | None):
        # NOTE: Consider whether null safety can be supported
        assert_type(c(User).age.not_.in_([value]), NotInCondition)
