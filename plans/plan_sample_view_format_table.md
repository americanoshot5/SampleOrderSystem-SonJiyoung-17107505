# plans/plan_sample_view_format_table.md

## Behavior

`format_sample_table(samples)`는 `Sample` 리스트를 받아, 헤더(ID/이름/평균생산시간/수율/재고)와 각 시료를 한 줄씩 표기한 표 형태의 문자열을 반환한다. 빈 리스트가 주어지면 "등록된 시료가 없습니다."를 반환한다.

## Test

- `test_format_sample_table_with_samples_includes_header_and_rows`: 시료 1개(`S-001`, "실리콘 웨이퍼", 0.5, 0.92, 100)로 호출 시, 반환 문자열에 헤더 문구("ID", "이름")와 `"S-001"`, `"실리콘 웨이퍼"` 값이 모두 포함되는지 확인.
- `test_format_sample_table_with_empty_list_returns_no_data_message`: 빈 리스트로 호출 시 `"등록된 시료가 없습니다."`를 그대로 반환하는지 확인.

## Approach

- `app/view/sample_view.py` 신설: `format_sample_table(samples: list[Sample]) -> str` 순수 함수.
- 콘솔 입출력(`input()`/`print()`)은 이 함수에 포함하지 않음 — 추후 `main.py`(또는 얇은 진입점)에서 `print(format_sample_table(...))` 형태로만 사용. 이렇게 분리해야 View 로직을 실제 콘솔 없이 단위 테스트할 수 있음.
- 등록/검색 결과 메시지 포맷팅, 입력 프롬프트 등은 이후 증분에서 별도로 다룸.
