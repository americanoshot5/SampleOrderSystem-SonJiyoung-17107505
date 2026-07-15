# plans/plan_production_controller_list_queue.md

## Behavior

`ProductionController.list_production_queue()`는 `PRODUCING` 상태의 주문만 FIFO 순서(`order_no` 오름차순)로 조회하여 View의 표 형식 문자열로 포맷해 반환한다.

## Test

`test_list_production_queue_returns_formatted_table_of_producing_orders`:
- 시료(`S-001`) 등록 후 주문 2개를 재고보다 많은 수량으로 접수하고 모두 승인하여 둘 다 `PRODUCING` 상태로 만든다.
- `controller.list_production_queue()` 호출 결과가 `format_order_table(order_repository.find_by_status("PRODUCING"))`과 동일한지 확인.
- 결과에 `ORD-0001`, `ORD-0002` 모두 포함되는지 확인.

## Approach

- `ProductionController.list_production_queue(self) -> str`: `self._order_repository.find_by_status("PRODUCING")` 결과를 `format_order_table()`에 전달해 반환.
