# plans/plan_release_controller_list_confirmed.md

## Behavior

`ReleaseController.list_confirmed_orders()`는 `CONFIRMED` 상태의 주문만 조회하여 View의 표 형식 문자열로 포맷해 반환한다.

## Test

`test_list_confirmed_orders_returns_formatted_table_of_confirmed_orders`:
- 시료(`S-001`) 등록 후 주문 2개를 접수하여 하나는 승인(재고 충분 -> `CONFIRMED`), 하나는 거절(`REJECTED`)한다.
- `controller.list_confirmed_orders()` 호출 결과가 `format_order_table(order_repository.find_by_status("CONFIRMED"))`과 동일한지 확인.
- 결과에 `CONFIRMED` 주문의 번호는 포함되고 거절된 주문 번호는 포함되지 않는지 확인.

## Approach

- `app/controller/release_controller.py` 신설: `ReleaseController(order_repository: OrderRepository)` 클래스.
  - `list_confirmed_orders(self) -> str`: `self._order_repository.find_by_status("CONFIRMED")` 결과를 `format_order_table()`에 전달해 반환.
