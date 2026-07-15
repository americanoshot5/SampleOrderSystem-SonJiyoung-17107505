# plans/plan_db_schema_init.md

## Behavior

`init_db(conn)`을 호출하면 아직 존재하지 않는 SQLite DB에 `samples`, `orders` 두 테이블이 생성된다 (이미 존재하면 그대로 유지되어 재실행해도 안전함).

## Test

`test_init_db_creates_samples_and_orders_tables`:
- 임시 SQLite 파일에 대해 `get_connection()`으로 연결을 얻고 `init_db(conn)`을 호출한다.
- `sqlite_master`에서 테이블 이름을 조회하여 `{"samples", "orders"}`가 모두 포함되어 있는지 확인한다.

## Approach

- `app/db.py` 모듈 신설.
  - `get_connection(db_path: Path) -> sqlite3.Connection`: 부모 디렉터리를 생성하고, `row_factory = sqlite3.Row`, `PRAGMA foreign_keys = ON`으로 연결 반환.
  - `init_db(conn) -> None`: `CREATE TABLE IF NOT EXISTS` 기반 스키마 스크립트 실행.
    - `samples(sample_id TEXT PRIMARY KEY, name TEXT NOT NULL, avg_production_time REAL NOT NULL, yield_rate REAL NOT NULL, stock_quantity INTEGER NOT NULL DEFAULT 0)`
    - `orders(order_no TEXT PRIMARY KEY, sample_id TEXT NOT NULL REFERENCES samples(sample_id), customer_name TEXT NOT NULL, quantity INTEGER NOT NULL, status TEXT NOT NULL DEFAULT 'RESERVED', created_at TEXT NOT NULL)`
- 생산 큐(production queue)를 위한 테이블/구조는 이번 증분 범위에서 제외 (Phase 4에서 별도 PLAN으로 다룸 — YAGNI).
- 테스트는 `tests/` 하위, 실제 구현은 `app/` 패키지 하위에 위치시킬 예정 (이후 증분에서 `app/model`, `app/view`, `app/controller` 하위 구조로 확장).
