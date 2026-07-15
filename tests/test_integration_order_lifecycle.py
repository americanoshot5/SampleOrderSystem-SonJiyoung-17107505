from pathlib import Path

from app.controller.monitoring_controller import MonitoringController
from app.controller.order_controller import OrderController
from app.controller.production_controller import ProductionController
from app.controller.release_controller import ReleaseController
from app.db import get_connection, init_db
from app.model.order_repository import OrderRepository
from app.model.sample import Sample
from app.model.sample_repository import SampleRepository


def test_full_lifecycle_with_sufficient_stock_reaches_release(tmp_path: Path):
    conn = get_connection(tmp_path / "test.db")
    try:
        init_db(conn)
        sample_repository = SampleRepository(conn)
        order_repository = OrderRepository(conn)
        order_controller = OrderController(sample_repository, order_repository)
        release_controller = ReleaseController(order_repository)
        monitoring_controller = MonitoringController(order_repository, sample_repository)

        sample_repository.create(
            Sample(
                sample_id="S-001",
                name="실리콘 웨이퍼",
                avg_production_time=0.5,
                yield_rate=0.92,
                stock_quantity=100,
            )
        )

        order_controller.place_order("S-001", "삼성전자", 30, "2026-07-16T00:00:00")
        assert order_repository.find_by_order_no("ORD-0001").status == "RESERVED"

        order_controller.approve_order("ORD-0001")
        assert order_repository.find_by_order_no("ORD-0001").status == "CONFIRMED"
        assert sample_repository.find_by_id("S-001").stock_quantity == 70

        status_summary = monitoring_controller.summarize_order_status()
        assert "CONFIRMED: 1" in status_summary
        assert "RESERVED: 0" in status_summary

        release_controller.release_order("ORD-0001")
        assert order_repository.find_by_order_no("ORD-0001").status == "RELEASE"

        final_summary = monitoring_controller.summarize_order_status()
        assert "RELEASE: 1" in final_summary
    finally:
        conn.close()


def test_full_lifecycle_with_insufficient_stock_reaches_release_after_production(tmp_path: Path):
    conn = get_connection(tmp_path / "test.db")
    try:
        init_db(conn)
        sample_repository = SampleRepository(conn)
        order_repository = OrderRepository(conn)
        order_controller = OrderController(sample_repository, order_repository)
        production_controller = ProductionController(sample_repository, order_repository)
        release_controller = ReleaseController(order_repository)
        monitoring_controller = MonitoringController(order_repository, sample_repository)

        sample_repository.create(
            Sample(
                sample_id="S-001",
                name="실리콘 웨이퍼",
                avg_production_time=0.5,
                yield_rate=0.92,
                stock_quantity=30,
            )
        )

        order_controller.place_order("S-001", "삼성전자", 50, "2026-07-16T00:00:00")

        order_controller.approve_order("ORD-0001")
        assert order_repository.find_by_order_no("ORD-0001").status == "PRODUCING"
        assert sample_repository.find_by_id("S-001").stock_quantity == 30

        production_controller.process_next_production()
        assert order_repository.find_by_order_no("ORD-0001").status == "CONFIRMED"
        assert sample_repository.find_by_id("S-001").stock_quantity == 2

        release_controller.release_order("ORD-0001")
        assert order_repository.find_by_order_no("ORD-0001").status == "RELEASE"

        final_summary = monitoring_controller.summarize_order_status()
        assert "RELEASE: 1" in final_summary
        assert "PRODUCING: 0" in final_summary
    finally:
        conn.close()
