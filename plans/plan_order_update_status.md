# plans/plan_order_update_status.md

## Behavior

`OrderRepository.update_status(order_no, status)`는 해당 주문의 `status`를 지정한 값으로 갱신한다.

## Test

`test_update_status_changes_order_status`:
- 시료(`S-001`) 등록 후 주문(`ORD-0001`, 상태 `RESERVED`) 생성.
- `repository.update_status("ORD-0001", "CONFIRMED")` 호출.
- `repository.find_by_order_no("ORD-0001").status == "CONFIRMED"`인지 확인.

## Approach

- `OrderRepository.update_status(self, order_no: str, status: str) -> None`: `UPDATE orders SET status = ? WHERE order_no = ?` 실행 후 commit.
- 존재하지 않는 order_no 처리(예외 등)는 이번 증분 범위 밖 (YAGNI — 항상 존재가 보장된 컨텍스트에서만 호출).
