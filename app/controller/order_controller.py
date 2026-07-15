from app.model.order import Order
from app.model.order_numbering import generate_next_order_no
from app.model.order_repository import OrderRepository
from app.model.order_status import CONFIRMED, PRODUCING, REJECTED, RESERVED
from app.model.sample_repository import SampleRepository
from app.view.order_view import format_order_table


class OrderController:
    def __init__(self, sample_repository: SampleRepository, order_repository: OrderRepository):
        self._sample_repository = sample_repository
        self._order_repository = order_repository

    def place_order(self, sample_id: str, customer_name: str, quantity: int, created_at: str) -> str:
        if self._sample_repository.find_by_id(sample_id) is None:
            return f"등록되지 않은 시료 ID입니다: {sample_id}"

        existing_order_nos = [order.order_no for order in self._order_repository.find_all()]
        order_no = generate_next_order_no(existing_order_nos)

        self._order_repository.create(
            Order(
                order_no=order_no,
                sample_id=sample_id,
                customer_name=customer_name,
                quantity=quantity,
                status=RESERVED,
                created_at=created_at,
            )
        )
        return f"예약 접수 완료. 주문번호: {order_no}"

    def approve_order(self, order_no: str) -> str:
        order = self._order_repository.find_by_order_no(order_no)
        sample = self._sample_repository.find_by_id(order.sample_id)

        if sample.stock_quantity >= order.quantity:
            self._sample_repository.update_stock(
                sample.sample_id, sample.stock_quantity - order.quantity
            )
            self._order_repository.update_status(order_no, CONFIRMED)
            return f"승인 완료. 주문 '{order_no}' 상태가 CONFIRMED로 전환되었습니다."

        shortage = order.quantity - sample.stock_quantity
        self._order_repository.update_status(order_no, PRODUCING)
        return (
            f"재고 부족으로 생산 대기 등록. 부족분: {shortage}. "
            f"주문 '{order_no}' 상태가 PRODUCING으로 전환되었습니다."
        )

    def reject_order(self, order_no: str) -> str:
        self._order_repository.update_status(order_no, REJECTED)
        return f"주문 '{order_no}'을(를) 거절했습니다."

    def list_reserved_orders(self) -> str:
        return format_order_table(self._order_repository.find_by_status(RESERVED))
