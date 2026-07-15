# plans/plan_sample_duplicate_id_validation.md

## Behavior

`SampleRepository.create()`에 이미 존재하는 `sample_id`를 가진 시료를 등록하려 하면 `ValueError`를 발생시키고, 기존 데이터는 변경되지 않는다.

## Test

`test_create_with_duplicate_sample_id_raises_value_error`:
- 시료(`S-001`)를 한 번 생성.
- 동일한 `sample_id`("S-001")를 가진(이름 등 다른 필드는 달라도 됨) 시료를 다시 `create()` 시도.
- `ValueError`가 발생하는지 확인.
- (부가 확인) `find_by_id("S-001")`로 조회했을 때 여전히 최초 등록된 값 그대로인지 확인.

## Approach

- `SampleRepository.create()` 시작 부분에 `self.find_by_id(sample.sample_id) is not None`인 경우 `ValueError(f"이미 존재하는 시료 ID입니다: {sample.sample_id}")`를 발생시키고 INSERT를 실행하지 않도록 가드 추가.
- 별도의 `exists()` 헬퍼는 도입하지 않고 기존 `find_by_id()`를 재사용 (YAGNI).
