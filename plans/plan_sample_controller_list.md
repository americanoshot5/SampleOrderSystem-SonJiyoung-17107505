# plans/plan_sample_controller_list.md

## Behavior

`SampleController.list_samples()`는 리포지토리에 등록된 모든 시료를 조회하여, View의 표 형식 문자열로 포맷해 반환한다.

## Test

`test_list_samples_returns_formatted_table_of_all_samples`:
- 시료 2개 등록.
- `controller.list_samples()` 호출 결과가 `format_sample_table(repository.find_all())`과 동일한 문자열인지 확인 (양쪽 시료의 ID가 모두 포함되는지도 함께 확인).

## Approach

- `SampleController.list_samples(self) -> str`: `self._repository.find_all()` 결과를 `format_sample_table()`에 전달해 반환.
- `app/controller/sample_controller.py`에 `from app.view.sample_view import format_sample_table` 임포트 추가.
