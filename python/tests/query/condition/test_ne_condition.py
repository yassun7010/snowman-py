from typing import assert_type

import pytest
from snowman.query.column import Column
from snowman.typing import TypeMissMatch, UseIsNotInsteadOfNe


class TestNeCondition:
    def test_ne_condition(self, int_column: Column[int]):
        condition = (int_column != 1).to_condition()
        assert condition.condition == "id != %s"
        assert condition.params == (1,)

    def test_eq_condition_type_miss_match(self, int_column: Column[int]):
        assert_type(int_column != "1", TypeMissMatch[int, str])

    @pytest.mark.parametrize("value", [True, False, None])
    def test_ne_condition_use_is(self, int_column: Column[int], value: bool | None):
        assert_type(int_column != value, UseIsNotInsteadOfNe)
