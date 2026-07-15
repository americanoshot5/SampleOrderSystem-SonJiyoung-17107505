# plans/plan_monitoring_order_status_summary.md

## Behavior

`MonitoringController.summarize_order_status()`는 `RESERVED`, `CONFIRMED`, `PRODUCING`, `RELEASE` 상태별 주문 건수를 표기한 문자열을 반환한다. `REJECTED`는 유효한 주문이 아니므로 집계에서 제외한다.

## Test

`test_summarize_order_status_excludes_rejected_and_counts_by_status`:
- 시료(`S-001`) 등록 후 주문 4개를 생성하여 각각 `RESERVED`, `CONFIRMED`, `PRODUCING`, `REJECTED` 상태가 되도록 만든다.
- `controller.summarize_order_status()` 호출 결과 문자열에 `RESERVED: 1`, `CONFIRMED: 1`, `PRODUCING: 1`, `RELEASE: 0`이 포함되는지 확인.
- 결과 문자열에 `REJECTED`라는 단어 자체가 포함되지 않는지 확인 (집계 대상 제외 검증).

## Approach

- `app/controller/monitoring_controller.py` 신설: `MonitoringController(order_repository: OrderRepository, sample_repository: SampleRepository)` 클래스.
  - `summarize_order_status(self) -> str`: `["RESERVED", "CONFIRMED", "PRODUCING", "RELEASE"]` 각 상태에 대해 `len(order_repository.find_by_status(status))`를 계산하여 `f"{status}: {count}"` 형태로 줄바꿈 결합.
- `REJECTED`는 순회 대상 리스트에 애초에 포함하지 않아 자연스럽게 제외.
