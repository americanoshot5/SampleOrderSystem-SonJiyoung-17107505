import sqlite3

from app.model.sample import Sample


class SampleRepository:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn

    def create(self, sample: Sample) -> None:
        self._conn.execute(
            "INSERT INTO samples (sample_id, name, avg_production_time, yield_rate, stock_quantity) "
            "VALUES (?, ?, ?, ?, ?)",
            (sample.sample_id, sample.name, sample.avg_production_time,
             sample.yield_rate, sample.stock_quantity),
        )
        self._conn.commit()

    def find_by_id(self, sample_id: str) -> Sample | None:
        row = self._conn.execute(
            "SELECT * FROM samples WHERE sample_id = ?", (sample_id,)
        ).fetchone()
        if row is None:
            return None
        return Sample(
            sample_id=row["sample_id"],
            name=row["name"],
            avg_production_time=row["avg_production_time"],
            yield_rate=row["yield_rate"],
            stock_quantity=row["stock_quantity"],
        )
