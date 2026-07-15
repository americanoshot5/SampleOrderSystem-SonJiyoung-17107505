# plans/plan_integration_happy_path.md

## Behavior

시료 등록 -> 주문 접수 -> 승인(재고 충분) -> 출고까지 전체 흐름이 실제 리포지토리/컨트롤러를 통해 끊김 없이 동작하고, 각 단계마다 DB 상태(주문 상태, 재고, 모니터링 집계)가 올바르게 반영된다.

## Test

`test_full_lifecycle_with_sufficient_stock_reaches_release`:
1. `SampleRepository`에 시료(`S-001`, 재고 100) 등록.
2. `OrderController.place_order()`로 수량 30 주문 접수 -> 상태 `RESERVED` 확인.
3. `OrderController.approve_order()` 호출 -> 상태 `CONFIRMED`, 재고 70(100-30)으로 차감 확인.
4. `MonitoringController.summarize_order_status()` 결과에 `CONFIRMED: 1`, `RESERVED: 0` 포함 확인.
5. `ReleaseController.release_order()` 호출 -> 상태 `RELEASE` 확인.
6. `MonitoringController.summarize_order_status()` 결과에 `RELEASE: 1` 포함 확인 (최종 상태 재확인).

## Approach

- `tests/test_integration_order_lifecycle.py` 신설.
- 실제 SQLite(tmp_path) + 모든 리포지토리/컨트롤러(SampleRepository, OrderRepository, OrderController, ReleaseController, MonitoringController)를 조합해 하나의 시나리오로 검증하는 통합 테스트 1개 작성.
- Mock 없이 실제 컴포넌트를 그대로 연결 (TDD 스킬의 "실제 코드 사용" 원칙 준수).
