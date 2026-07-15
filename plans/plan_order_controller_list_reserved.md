# plans/plan_order_controller_list_reserved.md

## Behavior

`OrderController.list_reserved_orders()`는 `RESERVED` 상태의 주문만 조회하여 View의 표 형식 문자열로 포맷해 반환한다.

## Test

`test_list_reserved_orders_returns_formatted_table_of_reserved_orders`:
- 시료(`S-001`) 등록 후 주문 2개 생성: `ORD-0001`(RESERVED로 유지), `ORD-0002`(승인 처리하여 CONFIRMED 또는 PRODUCING으로 전환).
- `controller.list_reserved_orders()` 호출 결과가 `format_order_table(order_repository.find_by_status("RESERVED"))`과 동일한지 확인.
- 결과에 `ORD-0001`은 포함되고 `ORD-0002`는 포함되지 않는지 확인.

## Approach

- `OrderController.list_reserved_orders(self) -> str`: `self._order_repository.find_by_status("RESERVED")` 결과를 `format_order_table()`에 전달해 반환.
