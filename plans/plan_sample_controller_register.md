# plans/plan_sample_controller_register.md

## Behavior

`SampleController.register_sample(sample)`은 리포지토리에 시료 등록을 시도하고, 성공하면 성공 메시지 문자열을, 이미 존재하는 ID로 실패하면 (예외를 전파하지 않고) 실패 메시지 문자열을 반환한다.

## Test

- `test_register_sample_success_returns_success_message`: 새 `Sample`로 `register_sample()` 호출 시 반환 메시지에 "등록 완료"가 포함되고, `repository.find_by_id()`로 실제 저장되었는지 확인.
- `test_register_duplicate_sample_returns_failure_message`: 동일 ID로 한 번 더 `register_sample()` 호출 시 예외가 아니라 "등록 실패"가 포함된 메시지를 반환하는지 확인 (예외 전파 없음).

## Approach

- `app/controller/sample_controller.py` 신설: `SampleController(repository: SampleRepository)` 클래스.
  - `register_sample(self, sample: Sample) -> str`: `repository.create(sample)` 호출을 `try/except ValueError`로 감싸, 성공 시 `f"시료 '{sample.name}' 등록 완료."`, 실패 시 `f"등록 실패: {e}"` 반환.
- Controller는 `input()`/`print()`를 직접 호출하지 않는다 — 파싱된 `Sample` 객체를 받아 결과 메시지를 반환하는 순수 로직만 담당. 실제 콘솔 입출력은 이후 `main.py`(얇은 진입점)에서 담당.
- 목록 조회(`list_samples`), 검색(`search_samples`) Controller 메서드는 각각 별도 증분으로 추가.
