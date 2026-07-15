# plans/plan_order_reject.md

## Behavior

`OrderController.reject_order(order_no)`은 재고 변경 없이 주문 상태를 `REJECTED`로 전환하고, 성공 메시지를 반환한다.

## Test

`test_reject_order_sets_rejected_without_changing_stock`:
- 시료(`S-001`, 재고 100)를 등록.
- 주문(`ORD-0001`, 수량 50, 상태 `RESERVED`)을 생성.
- `controller.reject_order("ORD-0001")` 호출.
- 반환 메시지에 "거절"이 포함되는지 확인.
- `order_repository.find_by_order_no("ORD-0001").status == "REJECTED"`인지 확인.
- `sample_repository.find_by_id("S-001").stock_quantity == 100`(변경 없음)인지 확인.

## Approach

- `OrderController.reject_order(self, order_no: str) -> str`: `order_repository.update_status(order_no, "REJECTED")` 실행 후 `f"주문 '{order_no}'을(를) 거절했습니다."` 반환. 재고는 건드리지 않는다.
