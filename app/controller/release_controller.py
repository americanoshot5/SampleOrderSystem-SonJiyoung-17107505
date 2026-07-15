from app.model.order_repository import OrderRepository
from app.view.order_view import format_order_table


class ReleaseController:
    def __init__(self, order_repository: OrderRepository):
        self._order_repository = order_repository

    def list_confirmed_orders(self) -> str:
        return format_order_table(self._order_repository.find_by_status("CONFIRMED"))

    def release_order(self, order_no: str) -> str:
        self._order_repository.update_status(order_no, "RELEASE")
        return f"주문 '{order_no}' 출고 완료."
