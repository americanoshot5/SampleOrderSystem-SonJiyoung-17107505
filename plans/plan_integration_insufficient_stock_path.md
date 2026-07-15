# plans/plan_integration_insufficient_stock_path.md

## Behavior

재고 부족 상황에서 시료 등록 -> 주문 접수 -> 승인(재고 부족 -> PRODUCING) -> 생산 처리(생산 완료 -> CONFIRMED, 재고 반영) -> 출고까지 전체 흐름이 실제 컴포넌트로 끊김 없이 동작한다.

## Test

`test_full_lifecycle_with_insufficient_stock_reaches_release_after_production`:
1. 시료(`S-001`, 재고 30, 평균생산시간 0.5, 수율 0.92) 등록.
2. `OrderController.place_order()`로 수량 50 주문 접수.
3. `OrderController.approve_order()` 호출 -> 상태 `PRODUCING`, 재고 30(변경 없음) 확인.
4. `ProductionController.process_next_production()` 호출 -> 상태 `CONFIRMED`, 재고 2(30+22-50) 확인 (부족분 20, 실생산량 `ceil(20/0.92)=22`).
5. `ReleaseController.release_order()` 호출 -> 상태 `RELEASE` 확인.
6. `MonitoringController.summarize_order_status()` 결과에 `RELEASE: 1`, `PRODUCING: 0` 포함 확인.

## Approach

- `tests/test_integration_order_lifecycle.py`에 두 번째 테스트 함수로 추가.
- `ProductionController`, `MonitoringController`까지 포함한 전체 컴포넌트 조합으로 시나리오 검증 (mock 없음).
