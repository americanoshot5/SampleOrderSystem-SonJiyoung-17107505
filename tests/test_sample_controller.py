from pathlib import Path

from app.controller.sample_controller import SampleController
from app.db import get_connection, init_db
from app.model.sample import Sample
from app.model.sample_repository import SampleRepository


def test_register_sample_success_returns_success_message(tmp_path: Path):
    conn = get_connection(tmp_path / "test.db")
    try:
        init_db(conn)
        repository = SampleRepository(conn)
        controller = SampleController(repository)
        sample = Sample(
            sample_id="S-001",
            name="실리콘 웨이퍼",
            avg_production_time=0.5,
            yield_rate=0.92,
            stock_quantity=100,
        )

        message = controller.register_sample(sample)

        assert "등록 완료" in message
        assert repository.find_by_id("S-001") == sample
    finally:
        conn.close()


def test_register_duplicate_sample_returns_failure_message(tmp_path: Path):
    conn = get_connection(tmp_path / "test.db")
    try:
        init_db(conn)
        repository = SampleRepository(conn)
        controller = SampleController(repository)
        sample = Sample(
            sample_id="S-001",
            name="실리콘 웨이퍼",
            avg_production_time=0.5,
            yield_rate=0.92,
            stock_quantity=100,
        )
        controller.register_sample(sample)

        message = controller.register_sample(sample)

        assert "등록 실패" in message
    finally:
        conn.close()
