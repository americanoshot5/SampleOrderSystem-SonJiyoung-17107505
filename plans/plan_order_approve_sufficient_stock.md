# plans/plan_order_approve_sufficient_stock.md

## Behavior

`OrderController.approve_order(order_no)`을 호출했을 때, 주문 수량이 시료의 현재 재고 이하(재고 충분)이면 재고를 주문 수량만큼 차감하고 주문 상태를 `CONFIRMED`로 전환한 뒤, 성공 메시지를 반환한다.

## Test

`test_approve_order_with_sufficient_stock_confirms_order_and_deducts_stock`:
- 시료(`S-001`, 재고 100)를 등록.
- 주문(`ORD-0001`, 수량 50, 상태 `RESERVED`)을 생성.
- `controller.approve_order("ORD-0001")` 호출.
- 반환 메시지에 "승인 완료"가 포함되는지 확인.
- `order_repository.find_by_order_no("ORD-0001").status == "CONFIRMED"`인지 확인.
- `sample_repository.find_by_id("S-001").stock_quantity == 50`(100 - 50)인지 확인.

## Approach

- `app/controller/order_controller.py`에 `OrderController.approve_order(self, order_no: str) -> str` 추가.
  1. `order_repository.find_by_order_no(order_no)`로 주문 조회 (없으면 이번 증분에서는 고려하지 않음 — 항상 존재하는 주문에 대해서만 호출된다고 가정, YAGNI).
  2. `sample_repository.find_by_id(order.sample_id)`로 시료 조회.
  3. `sample.stock_quantity >= order.quantity`이면(재고 충분): `sample_repository.update_stock(sample.sample_id, sample.stock_quantity - order.quantity)` 실행, `order_repository.update_status(order_no, "CONFIRMED")` 실행, `f"승인 완료. 주문 '{order_no}' 상태가 CONFIRMED로 전환되었습니다."` 반환.
- 재고 부족 분기(PRODUCING 전환)는 다음 증분에서 별도로 추가.
