from pathlib import Path

from app.db import get_connection, init_db
from app.model.order import Order
from app.model.order_repository import OrderRepository
from app.model.sample import Sample
from app.model.sample_repository import SampleRepository


def test_create_then_find_by_order_no_returns_same_order(tmp_path: Path):
    conn = get_connection(tmp_path / "test.db")
    try:
        init_db(conn)
        SampleRepository(conn).create(
            Sample(
                sample_id="S-001",
                name="실리콘 웨이퍼",
                avg_production_time=0.5,
                yield_rate=0.92,
                stock_quantity=100,
            )
        )
        repository = OrderRepository(conn)
        order = Order(
            order_no="ORD-0001",
            sample_id="S-001",
            customer_name="삼성전자",
            quantity=50,
            status="RESERVED",
            created_at="2026-07-16T00:00:00",
        )

        repository.create(order)
        found = repository.find_by_order_no("ORD-0001")

        assert found == order
    finally:
        conn.close()


def test_find_all_returns_all_orders_ordered_by_order_no(tmp_path: Path):
    conn = get_connection(tmp_path / "test.db")
    try:
        init_db(conn)
        SampleRepository(conn).create(
            Sample(
                sample_id="S-001",
                name="실리콘 웨이퍼",
                avg_production_time=0.5,
                yield_rate=0.92,
                stock_quantity=100,
            )
        )
        repository = OrderRepository(conn)
        order_2 = Order(
            order_no="ORD-0002",
            sample_id="S-001",
            customer_name="SK하이닉스",
            quantity=30,
            status="RESERVED",
            created_at="2026-07-16T01:00:00",
        )
        order_1 = Order(
            order_no="ORD-0001",
            sample_id="S-001",
            customer_name="삼성전자",
            quantity=50,
            status="RESERVED",
            created_at="2026-07-16T00:00:00",
        )
        repository.create(order_2)
        repository.create(order_1)

        assert repository.find_all() == [order_1, order_2]
    finally:
        conn.close()
