from typing import assert_type

import pytest
from conftest import User
from snowman.query.builder.condition.eq_condition import EqCondition
from snowman.query.expression import column as c
from snowman.typing import TypeMissMatch, UseIsInsteadOfEq


class TestEqCondition:
    def test_eq_condition(self):
        condition = c(User).id == 1
        sql = condition.to_sql()

        assert_type(condition, EqCondition)
        assert sql.operation == "id = %s"
        assert sql.params == (1,)

    def test_eq_condition_type_miss_match(self):
        assert_type(c(User).id == "1", TypeMissMatch[int, str])

    @pytest.mark.parametrize("value", [True, False, None])
    def test_eq_condition_use_is(self, value: bool | None):
        assert_type(c(User).id == value, UseIsInsteadOfEq)

    @pytest.mark.parametrize("value", [1, None])
    def test_eq_condition_use_nullable(self, value: int | None):
        # NOTE: Consider whether null safety can be supported
        assert_type(c(User).age == value, EqCondition)
