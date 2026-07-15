# plans/plan_sample_controller_search.md

## Behavior

`SampleController.search_samples(keyword)`는 리포지토리에서 이름에 `keyword`가 포함된 시료만 조회하여, View의 표 형식 문자열로 포맷해 반환한다.

## Test

`test_search_samples_returns_formatted_table_of_matching_samples`:
- 시료 2개 등록 ("실리콘 웨이퍼", "GaN 에피택셜").
- `controller.search_samples("실리콘")` 호출 결과가 `format_sample_table(repository.search_by_name("실리콘"))`과 동일한지 확인.
- 결과에 "S-001"은 포함되고 "S-002"는 포함되지 않는지 확인.

## Approach

- `SampleController.search_samples(self, keyword: str) -> str`: `self._repository.search_by_name(keyword)` 결과를 `format_sample_table()`에 전달해 반환.
