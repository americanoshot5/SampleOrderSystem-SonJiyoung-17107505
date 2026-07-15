# plans/plan_release_order.md

## Behavior

`ReleaseController.release_order(order_no)`은 주문 상태를 `RELEASE`로 전환하고, 성공 메시지를 반환한다.

## Test

`test_release_order_sets_release_status`:
- 시료(`S-001`, 재고 100)를 등록.
- 주문(`ORD-0001`, 수량 50)을 접수하고 승인하여 `CONFIRMED` 상태로 만든다.
- `controller.release_order("ORD-0001")` 호출.
- 반환 메시지에 "출고 완료"가 포함되는지 확인.
- `order_repository.find_by_order_no("ORD-0001").status == "RELEASE"`인지 확인.

## Approach

- `ReleaseController.release_order(self, order_no: str) -> str`: `order_repository.update_status(order_no, "RELEASE")` 실행 후 `f"주문 '{order_no}' 출고 완료."` 반환.
