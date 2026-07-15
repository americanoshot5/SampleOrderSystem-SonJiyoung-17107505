from app.model.order import Order


def format_order_table(orders: list[Order]) -> str:
    if not orders:
        return "주문이 없습니다."

    header = f"{'주문번호':<20}{'시료ID':<10}{'고객명':<15}{'수량':<8}{'상태':<12}"
    rows = [
        f"{o.order_no:<20}{o.sample_id:<10}{o.customer_name:<15}{o.quantity:<8}{o.status:<12}"
        for o in orders
    ]
    return "\n".join([header, *rows])
