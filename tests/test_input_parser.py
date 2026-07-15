from app.view.input_parser import parse_float, parse_int


def test_parse_int_with_valid_number_returns_int():
    assert parse_int("50") == 50


def test_parse_int_with_non_numeric_text_returns_none():
    assert parse_int("abc") is None


def test_parse_float_with_valid_number_returns_float():
    assert parse_float("0.92") == 0.92


def test_parse_float_with_non_numeric_text_returns_none():
    assert parse_float("abc") is None
