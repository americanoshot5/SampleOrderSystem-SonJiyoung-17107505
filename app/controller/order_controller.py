from app.model.order import Order
from app.model.order_numbering import generate_next_order_no
from app.model.order_repository import OrderRepository
from app.model.sample_repository import SampleRepository


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
                status="RESERVED",
                created_at=created_at,
            )
        )
        return f"예약 접수 완료. 주문번호: {order_no}"
