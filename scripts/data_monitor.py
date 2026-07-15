import argparse
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).parent.parent / "data" / "sample_order.db"
WATCH_INTERVAL_SECONDS = 2


class DataMonitor:
    """SQLite DB의 현재 상태를 조회하는 읽기 전용 모니터링 도구."""

    def __init__(self, db_path: Path):
        self._db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def list_tables(self) -> list[str]:
        conn = self._connect()
        try:
            rows = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' "
                "ORDER BY name"
            ).fetchall()
            return [row["name"] for row in rows]
        finally:
            conn.close()

    def get_row_count(self, table: str) -> int:
        conn = self._connect()
        try:
            return conn.execute(f"SELECT COUNT(*) AS cnt FROM {table}").fetchone()["cnt"]
        finally:
            conn.close()

    def get_columns(self, table: str) -> list[str]:
        conn = self._connect()
        try:
            rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
            return [row["name"] for row in rows]
        finally:
            conn.close()

    def get_rows(self, table: str, limit: int = 50) -> list[sqlite3.Row]:
        conn = self._connect()
        try:
            return conn.execute(f"SELECT * FROM {table} LIMIT ?", (limit,)).fetchall()
        finally:
            conn.close()

    def db_exists(self) -> bool:
        return self._db_path.exists()


def print_table(monitor: DataMonitor, table: str, limit: int = 50) -> None:
    columns = monitor.get_columns(table)
    rows = monitor.get_rows(table, limit)
    header = "".join(f"{col:<18}" for col in columns)
    print(header)
    print("-" * len(header))
    for row in rows:
        print("".join(f"{str(row[col]):<18}" for col in columns))
    print(f"(총 {monitor.get_row_count(table)}건)")


def show_summary(monitor: DataMonitor) -> None:
    tables = monitor.list_tables()
    if not tables:
        print("DB에 테이블이 없습니다.")
        return
    print(f"\n{'테이블':<20}{'행 수':<10}")
    for table in tables:
        print(f"{table:<20}{monitor.get_row_count(table):<10}")


def show_table_detail(monitor: DataMonitor) -> None:
    tables = monitor.list_tables()
    if not tables:
        print("DB에 테이블이 없습니다.")
        return
    for i, table in enumerate(tables, start=1):
        print(f"[{i}] {table}")
    choice = input("조회할 테이블 번호 > ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(tables)):
        print("올바른 번호를 선택하세요.")
        return
    table = tables[int(choice) - 1]
    print()
    print_table(monitor, table)


def watch_mode(monitor: DataMonitor) -> None:
    print("실시간 감시를 시작합니다. (Ctrl+C로 중단)")
    try:
        while True:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] DB 상태")
            show_summary(monitor)
            time.sleep(WATCH_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\n실시간 감시를 중단합니다.")


def show_menu() -> None:
    print("\n==================== DataMonitor ====================")
    print("[1] 테이블 요약(행 수)   [2] 테이블 상세 조회   [3] 실시간 감시   [0] 종료")


def parse_db_path() -> Path:
    parser = argparse.ArgumentParser(description="SQLite DB 실시간 모니터링 도구")
    parser.add_argument(
        "--db", type=str, default=str(DEFAULT_DB_PATH),
        help="모니터링할 SQLite DB 파일 경로 (기본값: ./data/sample_order.db)",
    )
    args = parser.parse_args()
    return Path(args.db)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

    db_path = parse_db_path()
    monitor = DataMonitor(db_path)

    if not monitor.db_exists():
        print(f"경고: DB 파일을 찾을 수 없습니다: {db_path}")
        print("--db 옵션으로 기존 SQLite DB 경로를 지정하거나, main.py를 먼저 실행해 DB를 생성하세요.")
        return

    actions = {
        "1": lambda: show_summary(monitor),
        "2": lambda: show_table_detail(monitor),
        "3": lambda: watch_mode(monitor),
    }

    while True:
        show_menu()
        choice = input("선택 > ").strip()
        if choice == "0":
            print("종료합니다.")
            return
        action = actions.get(choice)
        if action is None:
            print("올바른 메뉴를 선택하세요.")
            continue
        action()


if __name__ == "__main__":
    main()
