from pathlib import Path

from app.controller.order_controller import OrderController
from app.controller.production_controller import ProductionController
from app.db import get_connection, init_db
from app.model.order_repository import OrderRepository
from app.model.sample import Sample
from app.model.sample_repository import SampleRepository
from app.view.order_view import format_order_table


def test_process_next_production_with_empty_queue_returns_no_pending_message(tmp_path: Path):
    conn = get_connection(tmp_path / "test.db")
    try:
        init_db(conn)
        sample_repository = SampleRepository(conn)
        order_repository = OrderRepository(conn)
        controller = ProductionController(sample_repository, order_repository)

        message = controller.process_next_production()

        assert message == "생산 대기 중인 주문이 없습니다."
    finally:
        conn.close()


def test_process_next_production_completes_first_order_in_fifo_order(tmp_path: Path):
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
                stock_quantity=30,
            )
        )
        order_controller = OrderController(sample_repository, order_repository)
        order_controller.place_order("S-001", "삼성전자", 50, "2026-07-16T00:00:00")
        order_controller.place_order("S-001", "SK하이닉스", 40, "2026-07-16T01:00:00")
        order_controller.approve_order("ORD-0001")
        order_controller.approve_order("ORD-0002")

        controller = ProductionController(sample_repository, order_repository)
        message = controller.process_next_production()

        assert "생산 완료" in message
        assert "22" in message
        assert order_repository.find_by_order_no("ORD-0001").status == "CONFIRMED"
        assert sample_repository.find_by_id("S-001").stock_quantity == 2
        assert order_repository.find_by_order_no("ORD-0002").status == "PRODUCING"
    finally:
        conn.close()


def test_list_production_queue_returns_formatted_table_of_producing_orders(tmp_path: Path):
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
                stock_quantity=30,
            )
        )
        order_controller = OrderController(sample_repository, order_repository)
        order_controller.place_order("S-001", "삼성전자", 50, "2026-07-16T00:00:00")
        order_controller.place_order("S-001", "SK하이닉스", 40, "2026-07-16T01:00:00")
        order_controller.approve_order("ORD-0001")
        order_controller.approve_order("ORD-0002")

        controller = ProductionController(sample_repository, order_repository)
        result = controller.list_production_queue()

        assert result == format_order_table(order_repository.find_by_status("PRODUCING"))
        assert "ORD-0001" in result
        assert "ORD-0002" in result
    finally:
        conn.close()
