from app.model.order_numbering import generate_next_order_no


def test_generate_next_order_no_with_empty_list_returns_first_number():
    assert generate_next_order_no([]) == "ORD-0001"


def test_generate_next_order_no_returns_next_sequence_after_max_existing():
    assert generate_next_order_no(["ORD-0001", "ORD-0003"]) == "ORD-0004"
