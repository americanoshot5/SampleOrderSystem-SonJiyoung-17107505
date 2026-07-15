# plans/plan_sample_find_all.md

## Behavior

`SampleRepository.find_all()`은 등록된 모든 시료를 `sample_id` 오름차순으로 정렬된 리스트로 반환한다.

## Test

`test_find_all_returns_all_samples_ordered_by_id`:
- 시료를 등록 순서를 뒤섞어 두 개(`S-002`, `S-001`) 생성.
- `repository.find_all()` 호출 결과가 `[S-001, S-002]` 순서(정렬된 sample_id 오름차순)와 일치하는지 확인.

## Approach

- `SampleRepository.find_all(self) -> list[Sample]`: `SELECT * FROM samples ORDER BY sample_id` 실행 후 각 row를 `Sample`로 변환.
- row -> `Sample` 변환 로직은 `find_by_id`에 이미 있는 것과 동일한 패턴이지만, 현재 반복 횟수(2회)가 추출을 정당화할 만큼 많지 않으므로 이번 증분에서는 중복을 그대로 둔다 (REVIEW 단계에서 3회째 반복이 생기면 재검토).
