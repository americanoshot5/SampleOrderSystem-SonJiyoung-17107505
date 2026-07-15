# plans/plan_monitoring_stock_status_summary.md

## Behavior

`MonitoringController.summarize_stock_status()`는 등록된 모든 시료에 대해 `시료ID/이름/재고수량/상태(여유·부족·고갈)`를 한 줄씩 표기한 문자열을 반환한다. 상태는 해당 시료의 미완료 주문(`RESERVED`+`PRODUCING`) 수량 합계와 현재 재고를 `determine_stock_status()`로 비교해 판정한다.

## Test

`test_summarize_stock_status_shows_status_per_sample`:
- 시료 2개 등록: `S-001`(재고 100), `S-002`(재고 0).
- `S-001`에 대해 수량 30짜리 `RESERVED` 주문 1개를 접수 (재고 100 >= 30 -> "여유" 예상).
- `S-002`는 미완료 주문 없이 재고 0 -> "고갈" 예상.
- `controller.summarize_stock_status()` 호출 결과에 `"S-001"`과 `"여유"`가 같은 줄에, `"S-002"`와 `"고갈"`이 같은 줄에 포함되는지 확인.

## Approach

- `MonitoringController.summarize_stock_status(self) -> str`:
  1. `samples = self._sample_repository.find_all()`.
  2. 각 시료에 대해 `pending = sum(o.quantity for o in self._order_repository.find_all() if o.sample_id == sample.sample_id and o.status in ("RESERVED", "PRODUCING"))` 계산.
  3. `status = determine_stock_status(sample.stock_quantity, pending)`.
  4. `f"{sample.sample_id} {sample.name} 재고:{sample.stock_quantity} 상태:{status}"` 형태로 한 줄씩 만들어 결합.
- `OrderRepository.find_all()`을 재사용하여 시료별 필터링 — 시료 수가 많지 않은 콘솔 애플리케이션 규모이므로 별도의 `find_by_sample_id` 조회 메서드는 추가하지 않는다(YAGNI).
