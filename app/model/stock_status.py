def determine_stock_status(stock_quantity: int, pending_order_quantity: int) -> str:
    if stock_quantity == 0:
        return "고갈"
    if stock_quantity < pending_order_quantity:
        return "부족"
    return "여유"
