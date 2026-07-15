PREFIX = "ORD-"


def generate_next_order_no(existing_order_nos: list[str]) -> str:
    sequences = [
        int(order_no[len(PREFIX):])
        for order_no in existing_order_nos
        if order_no.startswith(PREFIX) and order_no[len(PREFIX):].isdigit()
    ]
    next_sequence = max(sequences, default=0) + 1
    return f"{PREFIX}{next_sequence:04d}"
