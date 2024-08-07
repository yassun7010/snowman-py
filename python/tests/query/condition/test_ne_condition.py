from typing import assert_type

from snowman.query.column import Column
from snowman.typing import TypeMissMatch


class TestNeCondition:
    def test_ne_condition(self, id_column: Column[int]):
        condition = (id_column != 1).to_condition()
        assert condition.condition == "id != %s"
        assert condition.params == (1,)

    def test_eq_condition_type_miss_match(self, id_column: Column[int]):
        assert_type(id_column != "1", TypeMissMatch[int, str])
