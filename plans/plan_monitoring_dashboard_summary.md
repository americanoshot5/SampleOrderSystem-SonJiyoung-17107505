# plans/plan_monitoring_dashboard_summary.md

## Behavior

`MonitoringController.summarize_dashboard()`는 메인 메뉴에 표시할 요약 정보(등록 시료 수, 총 재고, 전체 주문 수, 생산라인 대기 수)를 한 줄의 문자열로 반환한다.

## Test

`test_summarize_dashboard_shows_counts`:
- 시료 2개 등록 (재고 100, 50 -> 총 재고 150).
- 주문 2개를 접수하고, 하나는 재고 부족으로 승인하여 `PRODUCING`으로 만든다 (생산라인 대기 1건).
- `controller.summarize_dashboard()` 결과 문자열에 "등록 시료: 2", "총 재고: 150", "전체 주문: 2", "생산라인 대기: 1"이 모두 포함되는지 확인.

## Approach

- `MonitoringController.summarize_dashboard(self) -> str`:
  - `sample_count = len(sample_repository.find_all())`
  - `total_stock = sum(s.stock_quantity for s in sample_repository.find_all())`
  - `order_count = len(order_repository.find_all())`
  - `producing_count = len(order_repository.find_by_status("PRODUCING"))`
  - `f"등록 시료: {sample_count}   총 재고: {total_stock}   전체 주문: {order_count}   생산라인 대기: {producing_count}"` 형태로 반환.
