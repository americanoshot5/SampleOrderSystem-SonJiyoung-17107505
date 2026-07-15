# plans/plan_order_find_all.md

## Behavior

`OrderRepository.find_all()`은 등록된 모든 주문을 `order_no` 오름차순으로 정렬된 리스트로 반환한다.

## Test

`test_find_all_returns_all_orders_ordered_by_order_no`:
- 시료(`S-001`) 하나를 먼저 등록.
- 주문을 순서를 뒤섞어 두 개(`ORD-0002`, `ORD-0001`) 생성.
- `repository.find_all()` 결과가 `[ORD-0001, ORD-0002]` 순서와 일치하는지 확인.

## Approach

- `OrderRepository.find_all(self) -> list[Order]`: `SELECT * FROM orders ORDER BY order_no` 실행 후 각 row를 `Order`로 변환.
- row -> `Order` 변환 로직은 `find_by_order_no`에 이미 있는 것과 동일한 패턴이므로, `SampleRepository`에서 했던 것과 동일하게 `_to_order()` 헬퍼로 추출한다 (이미 중복 패턴이 검증되었으므로 이번엔 GREEN 단계에서 바로 추출).
