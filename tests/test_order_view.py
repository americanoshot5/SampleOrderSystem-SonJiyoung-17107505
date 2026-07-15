from app.model.order import Order
from app.view.order_view import format_order_table


def test_format_order_table_with_orders_includes_header_and_rows():
    orders = [
        Order(
            order_no="ORD-0001",
            sample_id="S-001",
            customer_name="삼성전자",
            quantity=50,
            status="RESERVED",
            created_at="2026-07-16T00:00:00",
        )
    ]

    result = format_order_table(orders)

    assert "주문번호" in result
    assert "상태" in result
    assert "ORD-0001" in result
    assert "삼성전자" in result
    assert "RESERVED" in result


def test_format_order_table_with_empty_list_returns_no_data_message():
    result = format_order_table([])

    assert result == "주문이 없습니다."
