from typing import assert_type

import pytest
from snowman.query.builder.condition.not_in_condition import NotInCondition
from snowman.query.column import Column


class TestNotInCondition:
    def test_not_in_condition(self, int_column: Column[int]):
        condition = int_column.not_.in_([1, 2])
        sql = condition.to_sql()

        assert_type(condition, NotInCondition)
        assert sql.operation == "id NOT IN (%s)"
        assert sql.params == ([1, 2],)

    @pytest.mark.parametrize("value", [1, None])
    def test_not_in_condition_use_nullable(
        self, int_nullable_column: Column[int | None], value: int | None
    ):
        # NOTE: Consider whether null safety can be supported
        assert_type(int_nullable_column.not_.in_([value]), NotInCondition)
