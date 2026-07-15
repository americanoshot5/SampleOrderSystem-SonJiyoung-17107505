# plans/plan_order_controller_place_order.md

## Behavior

`OrderController.place_order(sample_id, customer_name, quantity, created_at)`은
- 존재하지 않는 `sample_id`로 요청하면 주문을 생성하지 않고 실패 메시지를 반환한다.
- 존재하는 `sample_id`로 요청하면 새 주문번호를 채번하여 상태 `RESERVED`로 저장하고, 주문번호가 포함된 성공 메시지를 반환한다.

## Test

- `test_place_order_with_unknown_sample_id_returns_failure_message`: 시료를 등록하지 않은 상태에서 `place_order("S-999", "삼성전자", 50, "2026-07-16T00:00:00")` 호출 시 "등록되지 않은 시료" 등 실패 메시지를 반환하고, `order_repository.find_all()`이 여전히 빈 리스트인지 확인.
- `test_place_order_with_known_sample_id_creates_reserved_order`: 시료(`S-001`)를 등록한 뒤 `place_order("S-001", "삼성전자", 50, "2026-07-16T00:00:00")` 호출 시:
  - 반환 메시지에 "접수 완료"와 생성된 주문번호(`ORD-0001`)가 포함되는지 확인.
  - `order_repository.find_by_order_no("ORD-0001")`로 조회한 주문이 `sample_id="S-001"`, `customer_name="삼성전자"`, `quantity=50`, `status="RESERVED"`, `created_at="2026-07-16T00:00:00"`과 일치하는지 확인.

## Approach

- `app/controller/order_controller.py` 신설: `OrderController(sample_repository: SampleRepository, order_repository: OrderRepository)` 클래스.
  - `place_order(self, sample_id: str, customer_name: str, quantity: int, created_at: str) -> str`:
    1. `sample_repository.find_by_id(sample_id)`가 `None`이면 `f"등록되지 않은 시료 ID입니다: {sample_id}"` 반환하고 종료.
    2. `order_repository.find_all()`에서 기존 주문번호 목록을 뽑아 `generate_next_order_no()`로 다음 주문번호 생성.
    3. `Order(order_no=..., sample_id=sample_id, customer_name=customer_name, quantity=quantity, status="RESERVED", created_at=created_at)`를 만들어 `order_repository.create()`.
    4. `f"예약 접수 완료. 주문번호: {order_no}"` 형태의 성공 메시지 반환.
- `created_at`은 Controller가 직접 `datetime.now()`를 호출하지 않고 호출자(추후 `main.py`)로부터 주입받는다 — 순수 로직으로 유지해 테스트가 결정론적이 되도록 함.
