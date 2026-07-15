# plans/plan_integration_reject_path.md

## Behavior

시료 등록 -> 주문 접수 -> 거절까지의 흐름에서 재고는 전혀 변경되지 않고, 거절된 주문은 모니터링의 유효 주문 집계에서 제외된다.

## Test

`test_full_lifecycle_with_rejection_excludes_from_monitoring`:
1. 시료(`S-001`, 재고 100) 등록.
2. `OrderController.place_order()`로 수량 50 주문 접수.
3. `OrderController.reject_order()` 호출 -> 상태 `REJECTED` 확인, 재고 100(변경 없음) 확인.
4. `MonitoringController.summarize_order_status()` 결과에 `RESERVED: 0`, `CONFIRMED: 0`, `PRODUCING: 0`, `RELEASE: 0`이 모두 포함되고(즉 REJECTED 건이 어떤 유효 상태로도 집계되지 않음) `"REJECTED"` 문자열 자체는 결과에 없는지 확인.
5. `ReleaseController.list_confirmed_orders()` 결과에도 해당 주문번호가 포함되지 않는지 확인 (거절된 주문은 출고 대상이 아님).

## Approach

- `tests/test_integration_order_lifecycle.py`에 세 번째 테스트 함수로 추가.
- `ReleaseController`까지 포함해 거절된 주문이 이후 어떤 흐름에도 노출되지 않음을 검증 (mock 없음).
