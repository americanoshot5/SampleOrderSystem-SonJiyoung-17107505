# plans/plan_order_find_by_status.md

## Behavior

`OrderRepository.find_by_status(status)`는 지정한 상태를 가진 주문만 `order_no` 오름차순으로 반환한다.

## Test

`test_find_by_status_returns_only_matching_orders`:
- 시료(`S-001`) 등록 후 주문 2개 생성: `ORD-0001`(상태 `RESERVED`), `ORD-0002`(상태 `CONFIRMED`).
- `repository.find_by_status("RESERVED")` 호출 결과가 `[ORD-0001]`만 포함하는지 확인.

## Approach

- `OrderRepository.find_by_status(self, status: str) -> list[Order]`: `SELECT * FROM orders WHERE status = ? ORDER BY order_no` 실행 후 `_to_order()` 재사용.
