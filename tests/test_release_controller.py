from pathlib import Path

from app.controller.order_controller import OrderController
from app.controller.release_controller import ReleaseController
from app.db import get_connection, init_db
from app.model.order_repository import OrderRepository
from app.model.sample import Sample
from app.model.sample_repository import SampleRepository
from app.view.order_view import format_order_table


def test_list_confirmed_orders_returns_formatted_table_of_confirmed_orders(tmp_path: Path):
    conn = get_connection(tmp_path / "test.db")
    try:
        init_db(conn)
        sample_repository = SampleRepository(conn)
        order_repository = OrderRepository(conn)
        sample_repository.create(
            Sample(
                sample_id="S-001",
                name="실리콘 웨이퍼",
                avg_production_time=0.5,
                yield_rate=0.92,
                stock_quantity=100,
            )
        )
        order_controller = OrderController(sample_repository, order_repository)
        order_controller.place_order("S-001", "삼성전자", 50, "2026-07-16T00:00:00")
        order_controller.place_order("S-001", "SK하이닉스", 30, "2026-07-16T01:00:00")
        order_controller.approve_order("ORD-0001")
        order_controller.reject_order("ORD-0002")

        controller = ReleaseController(order_repository)
        result = controller.list_confirmed_orders()

        assert result == format_order_table(order_repository.find_by_status("CONFIRMED"))
        assert "ORD-0001" in result
        assert "ORD-0002" not in result
    finally:
        conn.close()
