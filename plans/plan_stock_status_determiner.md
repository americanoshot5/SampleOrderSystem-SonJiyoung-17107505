# plans/plan_stock_status_determiner.md

## Behavior

`determine_stock_status(stock_quantity, pending_order_quantity)`은 시료의 현재 재고 수량과 미완료 주문(RESERVED+PRODUCING) 수량 합계를 비교하여 재고 상태를 판정한다.
- 재고 수량이 0이면 `"고갈"`.
- 재고 수량이 미완료 주문 수량 합계보다 적으면(0은 아니지만 부족) `"부족"`.
- 그 외(재고 수량이 미완료 주문 수량 합계 이상, 미완료 주문이 없는 경우 포함)에는 `"여유"`.

## Test

- `test_determine_stock_status_returns_exhausted_when_stock_is_zero`: `determine_stock_status(0, 50)` -> `"고갈"`.
- `test_determine_stock_status_returns_insufficient_when_stock_below_pending`: `determine_stock_status(10, 50)` -> `"부족"`.
- `test_determine_stock_status_returns_sufficient_when_stock_covers_pending`: `determine_stock_status(100, 50)` -> `"여유"`.
- `test_determine_stock_status_returns_sufficient_when_no_pending_orders`: `determine_stock_status(10, 0)` -> `"여유"`.

## Approach

- `app/model/stock_status.py` 신설: `determine_stock_status(stock_quantity: int, pending_order_quantity: int) -> str` 순수 함수.
  - `stock_quantity == 0` -> `"고갈"`
  - `stock_quantity < pending_order_quantity` -> `"부족"`
  - 그 외 -> `"여유"`
