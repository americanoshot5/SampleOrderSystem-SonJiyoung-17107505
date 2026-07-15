# plans/plan_production_controller_process_next.md

## Behavior

`ProductionController.process_next_production()`은 생산 큐(상태 `PRODUCING`인 주문들, `order_no` 오름차순 = FIFO)의 맨 앞 주문 하나를 처리한다.
- 큐가 비어 있으면 "생산 대기 중인 주문이 없습니다." 메시지를 반환하고 아무것도 변경하지 않는다.
- 큐에 주문이 있으면: 현재 재고 대비 부족분을 계산하고, 실 생산량(`ceil(부족분/수율)`)만큼 생산하여 재고에 반영한 뒤(재고 = 기존 재고 + 실생산량 - 주문수량), 해당 주문 상태를 `CONFIRMED`로 전환하고, 실 생산량/총 생산시간이 포함된 성공 메시지를 반환한다.

## Test

- `test_process_next_production_with_empty_queue_returns_no_pending_message`: `PRODUCING` 상태 주문이 없는 상태에서 호출 시 "생산 대기 중인 주문이 없습니다."를 반환하는지 확인.
- `test_process_next_production_completes_first_order_in_fifo_order`:
  - 시료(`S-001`, 재고 30, 평균생산시간 0.5, 수율 0.92)를 등록.
  - 주문 2개를 접수하고 모두 승인하여 첫 번째 주문(`ORD-0001`, 수량 50)은 부족분 20으로 `PRODUCING`, 두 번째 주문(`ORD-0002`, 수량 10)은... (주의: 두 번째 주문 승인 시 재고가 이미 첫 주문에 의해 변경되지 않았으므로 재고 30 그대로 대비 판단됨 -> 수량 10은 재고 이하이므로 즉시 `CONFIRMED`가 될 수 있음. FIFO 큐에 2개 이상의 `PRODUCING` 주문을 만들기 위해 두 번째 주문 수량도 재고보다 크게(예: 40) 설정.)
  - `controller.process_next_production()` 호출 시 먼저 접수된 주문(`ORD-0001`)만 처리되는지 확인 (FIFO).
  - 반환 메시지에 "생산 완료"와 실 생산량(`ceil(20/0.92)=22`)이 포함되는지 확인.
  - `order_repository.find_by_order_no("ORD-0001").status == "CONFIRMED"`인지 확인.
  - `sample_repository.find_by_id("S-001").stock_quantity == 30 + 22 - 50 == 2`인지 확인.
  - 아직 처리되지 않은 두 번째 주문(`ORD-0002`)은 여전히 `PRODUCING` 상태인지 확인.

## Approach

- `app/controller/production_controller.py` 신설: `ProductionController(sample_repository, order_repository)` 클래스.
  - `process_next_production(self) -> str`:
    1. `order_repository.find_by_status("PRODUCING")`로 큐 조회 (이미 `order_no` 오름차순 = FIFO).
    2. 비어 있으면 `"생산 대기 중인 주문이 없습니다."` 반환.
    3. 첫 번째 주문을 큐 헤드로 사용: `sample = sample_repository.find_by_id(order.sample_id)`.
    4. `shortage = order.quantity - sample.stock_quantity` (0 이하 방지를 위해 `max(0, ...)` 적용하지는 않음 — 이 시점 주문은 항상 `PRODUCING`이므로 이론상 양수).
    5. `actual_production = calculate_actual_production(shortage, sample.yield_rate)`.
    6. `production_time = calculate_production_time(sample.avg_production_time, actual_production)`.
    7. `new_stock = sample.stock_quantity + actual_production - order.quantity` 로 재고 갱신.
    8. `order_repository.update_status(order.order_no, "CONFIRMED")`.
    9. 실 생산량과 생산시간이 포함된 성공 메시지 반환.
