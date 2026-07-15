# plans/plan_production_calculator.md

## Behavior

생산 라인에서 사용할 세 가지 순수 계산 함수를 제공한다.
- `calculate_actual_production(shortage, yield_rate)`: 부족분과 수율로부터 실 생산량을 `ceil(부족분 / 수율)`로 계산.
- `calculate_production_time(avg_production_time, actual_production)`: 평균 생산시간과 실 생산량의 곱으로 총 생산 시간을 계산.

## Test

- `test_calculate_actual_production_rounds_up`: `calculate_actual_production(170, 0.92)` -> `ceil(170/0.92)` = `185` (170/0.92 = 184.78... -> 185로 올림).
- `test_calculate_actual_production_exact_division`: `calculate_actual_production(46, 0.92)` -> `50` (46/0.92 = 50.0 정확히 나눠떨어지는 경우도 확인).
- `test_calculate_production_time_multiplies_avg_time_by_actual_production`: `calculate_production_time(0.8, 185)` -> `148.0` (0.8 * 185).

## Approach

- `app/model/production_calculator.py` 신설:
  - `calculate_actual_production(shortage: int, yield_rate: float) -> int`: `math.ceil(shortage / yield_rate)`.
  - `calculate_production_time(avg_production_time: float, actual_production: int) -> float`: `avg_production_time * actual_production`.
- 두 함수 모두 DB나 다른 모듈에 의존하지 않는 순수 함수로 작성해 단위 테스트가 쉽도록 함.
