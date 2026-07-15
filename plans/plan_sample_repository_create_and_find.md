# plans/plan_sample_repository_create_and_find.md

## Behavior

`SampleRepository.create(sample)`으로 시료를 저장하면, `find_by_id(sample_id)`로 동일한 필드값을 가진 `Sample`을 다시 조회할 수 있다.

## Test

`test_create_then_find_by_id_returns_same_sample`:
- `Sample(sample_id="S-001", name="실리콘 웨이퍼", avg_production_time=0.5, yield_rate=0.92, stock_quantity=100)`를 생성.
- `repository.create(sample)` 호출 후 `repository.find_by_id("S-001")`을 호출.
- 반환된 `Sample`의 모든 필드가 원본과 동일한지 확인.

## Approach

- `app/model/sample.py`: `Sample` dataclass 신설 (`sample_id`, `name`, `avg_production_time`, `yield_rate`, `stock_quantity=0`).
- `app/model/sample_repository.py`: `SampleRepository(conn)` 클래스.
  - `create(sample: Sample) -> None`: `INSERT INTO samples (...) VALUES (...)` 후 commit.
  - `find_by_id(sample_id: str) -> Sample | None`: `SELECT * FROM samples WHERE sample_id = ?` 후 row를 `Sample`로 변환. 없으면 `None`.
- 목록 조회(`find_all`)와 이름 검색(`search_by_name`)은 Phase 1(시료 관리 기능)에서 실제 조회/검색 기능을 만들 때 별도 증분으로 추가 (YAGNI — 이번 증분은 영속성 라운드트립 검증에 집중).
- 중복 ID 등록 시 예외 처리도 Phase 1에서 다룸 (이번 테스트는 정상 케이스만 다룸).
