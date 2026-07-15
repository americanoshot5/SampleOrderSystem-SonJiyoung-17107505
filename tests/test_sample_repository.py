from pathlib import Path

import pytest

from app.db import get_connection, init_db
from app.model.sample import Sample
from app.model.sample_repository import SampleRepository


def test_create_then_find_by_id_returns_same_sample(tmp_path: Path):
    conn = get_connection(tmp_path / "test.db")
    try:
        init_db(conn)
        repository = SampleRepository(conn)
        sample = Sample(
            sample_id="S-001",
            name="실리콘 웨이퍼",
            avg_production_time=0.5,
            yield_rate=0.92,
            stock_quantity=100,
        )

        repository.create(sample)
        found = repository.find_by_id("S-001")

        assert found == sample
    finally:
        conn.close()


def test_create_with_duplicate_sample_id_raises_value_error(tmp_path: Path):
    conn = get_connection(tmp_path / "test.db")
    try:
        init_db(conn)
        repository = SampleRepository(conn)
        original = Sample(
            sample_id="S-001",
            name="실리콘 웨이퍼",
            avg_production_time=0.5,
            yield_rate=0.92,
            stock_quantity=100,
        )
        repository.create(original)

        duplicate = Sample(
            sample_id="S-001",
            name="다른 이름",
            avg_production_time=0.1,
            yield_rate=0.5,
            stock_quantity=1,
        )

        with pytest.raises(ValueError):
            repository.create(duplicate)

        assert repository.find_by_id("S-001") == original
    finally:
        conn.close()


def test_find_all_returns_all_samples_ordered_by_id(tmp_path: Path):
    conn = get_connection(tmp_path / "test.db")
    try:
        init_db(conn)
        repository = SampleRepository(conn)
        sample_2 = Sample(
            sample_id="S-002",
            name="GaN 에피택셜",
            avg_production_time=0.3,
            yield_rate=0.78,
            stock_quantity=220,
        )
        sample_1 = Sample(
            sample_id="S-001",
            name="실리콘 웨이퍼",
            avg_production_time=0.5,
            yield_rate=0.92,
            stock_quantity=100,
        )
        repository.create(sample_2)
        repository.create(sample_1)

        assert repository.find_all() == [sample_1, sample_2]
    finally:
        conn.close()
