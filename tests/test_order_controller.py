from pathlib import Path

from app.controller.order_controller import OrderController
from app.db import get_connection, init_db
from app.model.order_repository import OrderRepository
from app.model.sample import Sample
from app.model.sample_repository import SampleRepository


def test_place_order_with_unknown_sample_id_returns_failure_message(tmp_path: Path):
    conn = get_connection(tmp_path / "test.db")
    try:
        init_db(conn)
        sample_repository = SampleRepository(conn)
        order_repository = OrderRepository(conn)
        controller = OrderController(sample_repository, order_repository)

        message = controller.place_order("S-999", "삼성전자", 50, "2026-07-16T00:00:00")

        assert "등록되지 않은 시료" in message
        assert order_repository.find_all() == []
    finally:
        conn.close()


def test_place_order_with_known_sample_id_creates_reserved_order(tmp_path: Path):
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
        controller = OrderController(sample_repository, order_repository)

        message = controller.place_order("S-001", "삼성전자", 50, "2026-07-16T00:00:00")

        assert "접수 완료" in message
        assert "ORD-0001" in message
        order = order_repository.find_by_order_no("ORD-0001")
        assert order.sample_id == "S-001"
        assert order.customer_name == "삼성전자"
        assert order.quantity == 50
        assert order.status == "RESERVED"
        assert order.created_at == "2026-07-16T00:00:00"
    finally:
        conn.close()


def test_approve_order_with_sufficient_stock_confirms_order_and_deducts_stock(tmp_path: Path):
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
        controller = OrderController(sample_repository, order_repository)
        controller.place_order("S-001", "삼성전자", 50, "2026-07-16T00:00:00")

        message = controller.approve_order("ORD-0001")

        assert "승인 완료" in message
        assert order_repository.find_by_order_no("ORD-0001").status == "CONFIRMED"
        assert sample_repository.find_by_id("S-001").stock_quantity == 50
    finally:
        conn.close()
