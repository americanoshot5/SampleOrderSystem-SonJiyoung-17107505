# plans/plan_order_view_format_table.md

## Behavior

`format_order_table(orders)`는 `Order` 리스트를 받아, 헤더(주문번호/시료ID/고객명/수량/상태)와 각 주문을 한 줄씩 표기한 표 형태의 문자열을 반환한다. 빈 리스트가 주어지면 "주문이 없습니다."를 반환한다.

## Test

- `test_format_order_table_with_orders_includes_header_and_rows`: 주문 1개(`ORD-0001`, `S-001`, "삼성전자", 50, `RESERVED`)로 호출 시, 반환 문자열에 헤더 문구("주문번호", "상태")와 `"ORD-0001"`, `"삼성전자"`, `"RESERVED"` 값이 모두 포함되는지 확인.
- `test_format_order_table_with_empty_list_returns_no_data_message`: 빈 리스트로 호출 시 `"주문이 없습니다."`를 그대로 반환하는지 확인.

## Approach

- `app/view/order_view.py` 신설: `format_order_table(orders: list[Order]) -> str` 순수 함수 (`format_sample_table`과 동일한 패턴).
