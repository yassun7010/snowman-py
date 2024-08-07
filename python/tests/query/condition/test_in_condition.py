from typing import assert_type

import pytest
from snowman.query.builder.condition.in_condition import InCondition
from snowman.query.column import Column


class TestInCondition:
    def test_in_condition(self, int_column: Column[int]):
        condition = int_column.in_([1, 2])
        sql = condition.to_sql()

        assert_type(condition, InCondition)
        assert sql.condition == "id IN (%s)"
        assert sql.params == ([1, 2],)

    @pytest.mark.parametrize("value", [1, None])
    def test_in_condition_use_nullable(
        self, int_nullable_column: Column[int | None], value: int | None
    ):
        # NOTE: Consider whether null safety can be supported
        assert_type(int_nullable_column.in_([value]), InCondition)
