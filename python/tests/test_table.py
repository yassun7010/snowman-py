from conftest import UpperCaseTable, User


class TestTable:
    def test_constructor(self):
        User(id=1, name="Alice")

    def test_upper_case_table(self):
        UpperCaseTable(id=1, name="Alice")
        UpperCaseTable(ID=1, NAME="Alice")  # type: ignore
