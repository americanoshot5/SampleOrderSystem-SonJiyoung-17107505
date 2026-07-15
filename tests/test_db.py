from pathlib import Path

from app.db import get_connection, init_db


def test_init_db_creates_samples_and_orders_tables(tmp_path: Path):
    db_path = tmp_path / "test.db"
    conn = get_connection(db_path)
    try:
        init_db(conn)
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        table_names = {row["name"] for row in rows}
        assert {"samples", "orders"}.issubset(table_names)
    finally:
        conn.close()
