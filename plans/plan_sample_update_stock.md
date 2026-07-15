# plans/plan_sample_update_stock.md

## Behavior

`SampleRepository.update_stock(sample_id, new_quantity)`은 해당 시료의 `stock_quantity`를 지정한 값으로 갱신한다.

## Test

`test_update_stock_changes_stock_quantity`:
- 시료(`S-001`, 초기 재고 100)를 등록.
- `repository.update_stock("S-001", 50)` 호출.
- `repository.find_by_id("S-001").stock_quantity == 50`인지 확인.

## Approach

- `SampleRepository.update_stock(self, sample_id: str, new_quantity: int) -> None`: `UPDATE samples SET stock_quantity = ? WHERE sample_id = ?` 실행 후 commit.
- 존재하지 않는 sample_id에 대한 처리(예외 등)는 이번 증분 범위 밖 — 승인 로직에서는 항상 존재가 보장된 시료에 대해서만 호출하므로 별도 검증 없이 단순 UPDATE로 충분 (YAGNI).
