# plans/plan_input_parsing.md

## Behavior

`parse_int(text)`와 `parse_float(text)`는 사용자 입력 문자열을 각각 `int`/`float`로 변환하되, 변환할 수 없는 값이면 예외를 던지지 않고 `None`을 반환한다.

## Test

- `test_parse_int_with_valid_number_returns_int`: `parse_int("50")` -> `50`.
- `test_parse_int_with_non_numeric_text_returns_none`: `parse_int("abc")` -> `None`.
- `test_parse_float_with_valid_number_returns_float`: `parse_float("0.92")` -> `0.92`.
- `test_parse_float_with_non_numeric_text_returns_none`: `parse_float("abc")` -> `None`.

## Approach

- `app/view/input_parser.py` 신설:
  - `parse_int(text: str) -> int | None`: `try: return int(text) except ValueError: return None`.
  - `parse_float(text: str) -> float | None`: `try: return float(text) except ValueError: return None`.
- 이 두 함수는 순수 함수로, `main.py`에서 `input()`으로 받은 문자열을 넘겨 반복 재입력을 유도하는 용도로 사용될 예정 (다음 증분에서 `main.py`에 실제로 연결).
