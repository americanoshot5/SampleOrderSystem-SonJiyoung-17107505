from pathlib import Path

from app.controller.monitoring_controller import MonitoringController
from app.controller.order_controller import OrderController
from app.db import get_connection, init_db
from app.model.order_repository import OrderRepository
from app.model.sample import Sample
from app.model.sample_repository import SampleRepository


def test_summarize_order_status_excludes_rejected_and_counts_by_status(tmp_path: Path):
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
        order_controller.place_order("S-001", "고객A", 10, "2026-07-16T00:00:00")  # RESERVED로 유지
        order_controller.place_order("S-001", "고객B", 5, "2026-07-16T01:00:00")
        order_controller.approve_order("ORD-0002")  # 재고 충분 -> CONFIRMED
        order_controller.place_order("S-001", "고객C", 200, "2026-07-16T02:00:00")
        order_controller.approve_order("ORD-0003")  # 재고 부족 -> PRODUCING
        order_controller.place_order("S-001", "고객D", 1, "2026-07-16T03:00:00")
        order_controller.reject_order("ORD-0004")  # REJECTED

        controller = MonitoringController(order_repository, sample_repository)
        result = controller.summarize_order_status()

        assert "RESERVED: 1" in result
        assert "CONFIRMED: 1" in result
        assert "PRODUCING: 1" in result
        assert "RELEASE: 0" in result
        assert "REJECTED" not in result
    finally:
        conn.close()


def test_summarize_stock_status_shows_status_per_sample(tmp_path: Path):
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
        sample_repository.create(
            Sample(
                sample_id="S-002",
                name="산화막 웨이퍼",
                avg_production_time=0.6,
                yield_rate=0.88,
                stock_quantity=0,
            )
        )
        order_controller = OrderController(sample_repository, order_repository)
        order_controller.place_order("S-001", "고객A", 30, "2026-07-16T00:00:00")

        controller = MonitoringController(order_repository, sample_repository)
        result = controller.summarize_stock_status()

        s001_line = next(line for line in result.splitlines() if "S-001" in line)
        s002_line = next(line for line in result.splitlines() if "S-002" in line)
        assert "여유" in s001_line
        assert "고갈" in s002_line
    finally:
        conn.close()
