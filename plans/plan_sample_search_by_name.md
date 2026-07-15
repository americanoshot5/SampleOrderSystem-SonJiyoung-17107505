# plans/plan_sample_search_by_name.md

## Behavior

`SampleRepository.search_by_name(keyword)`은 이름에 `keyword`가 대소문자 구분 없이 부분 포함된 시료만 `sample_id` 오름차순으로 반환한다.

## Test

`test_search_by_name_returns_only_matching_samples`:
- 시료 3개 등록: `S-001`("실리콘 웨이퍼"), `S-002`("GaN 에피택셜"), `S-003`("실리콘 카바이드")
- `repository.search_by_name("실리콘")` 호출 결과가 `[S-001, S-003]`(이름에 "실리콘" 포함, id 오름차순)과 일치하는지 확인.

## Approach

- `SampleRepository.search_by_name(self, keyword: str) -> list[Sample]`: `SELECT * FROM samples WHERE name LIKE ? ORDER BY sample_id` (파라미터: `f"%{keyword}%"`) 실행 후 `_to_sample()` 재사용.
- SQLite `LIKE`는 기본적으로 ASCII 대소문자만 무시하지만, 한글 검색어이므로 대소문자 이슈가 실질적으로 없어 별도 `LOWER()` 처리는 이번 증분에서 생략 (필요 시 영문 대소문자 케이스가 요구될 때 별도 증분으로 추가).
