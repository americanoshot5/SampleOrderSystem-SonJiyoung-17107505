# plans/plan_order_approve_insufficient_stock.md

## Behavior

`OrderController.approve_order(order_no)`을 호출했을 때, 주문 수량이 시료의 현재 재고보다 많으면(재고 부족) 재고는 변경하지 않고 주문 상태를 `PRODUCING`으로 전환한 뒤, 부족분 정보가 포함된 안내 메시지를 반환한다.

## Test

`test_approve_order_with_insufficient_stock_sets_producing_without_changing_stock`:
- 시료(`S-001`, 재고 30)를 등록.
- 주문(`ORD-0001`, 수량 50, 상태 `RESERVED`)을 생성.
- `controller.approve_order("ORD-0001")` 호출.
- 반환 메시지에 "생산"과 부족분(`20`)이 포함되는지 확인.
- `order_repository.find_by_order_no("ORD-0001").status == "PRODUCING"`인지 확인.
- `sample_repository.find_by_id("S-001").stock_quantity == 30`(변경 없음)인지 확인.

## Approach

- 기존 `approve_order`의 `if sample.stock_quantity >= order.quantity:` 분기에 `else` 절 추가.
  - `shortage = order.quantity - sample.stock_quantity` 계산.
  - `order_repository.update_status(order_no, "PRODUCING")` 실행 (재고는 변경하지 않음 — 실제 생산/재고 반영은 Phase 4의 몫).
  - `f"재고 부족으로 생산 대기 등록. 부족분: {shortage}. 주문 '{order_no}' 상태가 PRODUCING으로 전환되었습니다."` 반환.
- 생산 큐 자체(FIFO 처리, 실 생산량 계산 등)는 Phase 4에서 다룬다 — 이번 증분은 상태 전환과 안내 메시지까지만 담당.
