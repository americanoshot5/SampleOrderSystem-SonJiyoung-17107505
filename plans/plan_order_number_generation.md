# plans/plan_order_number_generation.md

## Behavior

`generate_next_order_no(existing_order_nos)`는 기존 주문번호 목록(`ORD-0001` 형식)을 받아, 가장 큰 순번보다 1 큰 순번으로 다음 주문번호(`ORD-{seq:04d}`)를 반환한다. 기존 목록이 비어 있으면 `ORD-0001`을 반환한다.

## Test

- `test_generate_next_order_no_with_empty_list_returns_first_number`: `generate_next_order_no([])` -> `"ORD-0001"`.
- `test_generate_next_order_no_returns_next_sequence_after_max_existing`: `generate_next_order_no(["ORD-0001", "ORD-0003"])` -> `"ORD-0004"` (기존 중 최댓값 기준 +1, 순서 무관).

## Approach

- `app/model/order_numbering.py` 신설: `generate_next_order_no(existing_order_nos: list[str]) -> str` 순수 함수.
  - `"ORD-"` 접두사를 제거하고 정수로 변환 가능한 항목만 순번 후보로 취급, 최댓값 + 1을 4자리 zero-padding으로 포맷.
  - 후보가 없으면(빈 리스트) 1부터 시작.
- 이 함수는 DB에 의존하지 않는 순수 함수로 두어 단위 테스트가 쉽도록 함. 실제 사용 시에는 `OrderController`가 `order_repository.find_all()`(추후 증분에서 추가) 등으로 얻은 기존 주문번호 목록을 넘겨 호출한다.
