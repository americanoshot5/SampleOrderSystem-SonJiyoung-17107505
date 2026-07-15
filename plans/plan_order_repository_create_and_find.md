# plans/plan_order_repository_create_and_find.md

## Behavior

`OrderRepository.create(order)`으로 주문을 저장하면, `find_by_order_no(order_no)`로 동일한 필드값을 가진 `Order`를 다시 조회할 수 있다.

## Test

`test_create_then_find_by_order_no_returns_same_order`:
- 먼저 `SampleRepository`로 시료(`S-001`)를 하나 생성해둔다 (주문의 FK 대상).
- `Order(order_no="ORD-0001", sample_id="S-001", customer_name="삼성전자", quantity=50, status="RESERVED", created_at="2026-07-16T00:00:00")`를 생성.
- `repository.create(order)` 호출 후 `repository.find_by_order_no("ORD-0001")`을 호출.
- 반환된 `Order`의 모든 필드가 원본과 동일한지 확인.

## Approach

- `app/model/order.py`: `Order` dataclass 신설 (`order_no`, `sample_id`, `customer_name`, `quantity`, `status="RESERVED"`, `created_at`).
- `app/model/order_repository.py`: `OrderRepository(conn)` 클래스.
  - `create(order: Order) -> None`: `INSERT INTO orders (...) VALUES (...)` 후 commit.
  - `find_by_order_no(order_no: str) -> Order | None`: `SELECT * FROM orders WHERE order_no = ?` 후 row를 `Order`로 변환. 없으면 `None`.
- 상태별 목록 조회(`find_by_status`), 상태 전이(`update_status`), 재고 갱신 등은 이후 Phase(2~6)에서 실제 기능을 만들 때 별도 증분으로 추가 (YAGNI — 이번 증분은 영속성 라운드트립 검증에 집중).
