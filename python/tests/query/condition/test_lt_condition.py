from typing import assert_type

import pytest
from snowman.query.builder.condition.lt_condition import LtCondition
from snowman.query.column import Column
from snowman.typing import TypeMissMatch, UseIsInsteadOfEq


class TestLtCondition:
    def test_lt_condition(self, int_column: Column[int]):
        condition = int_column < 1
        sql = condition.to_sql()

        assert_type(condition, LtCondition)
        assert sql.condition == "id < %s"
        assert sql.params == (1,)

    def test_lt_condition_type_miss_match(self, int_column: Column[int]):
        assert_type(int_column == "1", TypeMissMatch[int, str])

    @pytest.mark.parametrize("value", [True, False, None])
    def test_lt_condition_use_is(self, int_column: Column[int], value: bool | None):
        assert_type(int_column == value, UseIsInsteadOfEq)

    @pytest.mark.parametrize("value", [1, None])
    def test_lt_condition_use_nullable(
        self, int_nullable_column: Column[int | None], value: int | None
    ):
        # NOTE: Consider whether null safety can be supported
        assert_type(int_nullable_column < value, LtCondition)
