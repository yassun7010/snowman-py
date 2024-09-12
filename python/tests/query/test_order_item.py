from conftest import User
from snowman.query.expression import column as c
from snowman.query.order_item import ColumnOrderItem


class TestOrderItem:
    def test_order_item(self):
        query, params = ColumnOrderItem(c(User).id).to_sql()
        assert query == "id"
        assert params == ()

    def test_asc_order_item_asc(self):
        query, params = ColumnOrderItem(c(User).id).asc.to_sql()
        assert query == "id ASC"
        assert params == ()

    def test_desc_order_item_desc(self):
        query, params = ColumnOrderItem(c(User).id).desc.to_sql()
        assert query == "id DESC"
        assert params == ()

    def test_asc_order_item_nulls_first(self):
        query, params = ColumnOrderItem(c(User).id).nulls.first.to_sql()
        assert query == "id NULLS FIRST"
        assert params == ()

    def test_desc_order_item_nulls_last(self):
        query, params = ColumnOrderItem(c(User).id).nulls.last.to_sql()
        assert query == "id NULLS LAST"
        assert params == ()

    def test_asc_order_item_asc_nulls_first(self):
        query, params = ColumnOrderItem(c(User).id).asc.nulls.first.to_sql()
        assert query == "id ASC NULLS FIRST"
        assert params == ()

    def test_desc_order_item_desc_nulls_first(self):
        query, params = ColumnOrderItem(c(User).id).desc.nulls.first.to_sql()
        assert query == "id DESC NULLS FIRST"
        assert params == ()

    def test_desc_order_item_asc_nulls_last(self):
        query, params = ColumnOrderItem(c(User).id).asc.nulls.last.to_sql()
        assert query == "id ASC NULLS LAST"
        assert params == ()

    def test_desc_order_item_desc_nulls_last(self):
        query, params = ColumnOrderItem(c(User).id).desc.nulls.last.to_sql()
        assert query == "id DESC NULLS LAST"
        assert params == ()
