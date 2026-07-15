from app.model.stock_status import determine_stock_status


def test_determine_stock_status_returns_exhausted_when_stock_is_zero():
    assert determine_stock_status(0, 50) == "고갈"


def test_determine_stock_status_returns_insufficient_when_stock_below_pending():
    assert determine_stock_status(10, 50) == "부족"


def test_determine_stock_status_returns_sufficient_when_stock_covers_pending():
    assert determine_stock_status(100, 50) == "여유"


def test_determine_stock_status_returns_sufficient_when_no_pending_orders():
    assert determine_stock_status(10, 0) == "여유"
