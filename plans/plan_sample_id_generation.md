# plans/plan_sample_id_generation.md

## Behavior

`generate_next_sample_id(existing_sample_ids)`는 기존 시료 ID 목록(`S-001` 형식)을 받아, 가장 큰 순번보다 1 큰 순번으로 다음 시료 ID(`S-{seq:03d}`)를 반환한다. 기존 목록이 비어 있으면 `S-001`을 반환한다.

## Test

- `test_generate_next_sample_id_with_empty_list_returns_first_id`: `generate_next_sample_id([])` -> `"S-001"`.
- `test_generate_next_sample_id_returns_next_sequence_after_max_existing`: `generate_next_sample_id(["S-001", "S-003"])` -> `"S-004"` (기존 중 최댓값 기준 +1, 순서 무관).

## Approach

- `app/model/sample_numbering.py` 신설: `generate_next_sample_id(existing_sample_ids: list[str]) -> str` 순수 함수.
  - `app/model/order_numbering.py`의 `generate_next_order_no`와 동일한 구조(접두사 `"S-"`, 3자리 zero-padding)로 구현.
- DummyDataGenerator 도구(Phase 8의 다음 단계, TDD 예외)에서 이 함수를 사용해 시료 ID를 자동 채번할 예정.
