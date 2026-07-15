from app.model.order_repository import OrderRepository
from app.model.order_status import CONFIRMED, PRODUCING
from app.model.production_calculator import (
    calculate_actual_production,
    calculate_production_time,
)
from app.model.sample_repository import SampleRepository
from app.view.order_view import format_order_table


class ProductionController:
    def __init__(self, sample_repository: SampleRepository, order_repository: OrderRepository):
        self._sample_repository = sample_repository
        self._order_repository = order_repository

    def process_next_production(self) -> str:
        queue = self._order_repository.find_by_status(PRODUCING)
        if not queue:
            return "생산 대기 중인 주문이 없습니다."

        order = queue[0]
        sample = self._sample_repository.find_by_id(order.sample_id)

        shortage = order.quantity - sample.stock_quantity
        actual_production = calculate_actual_production(shortage, sample.yield_rate)
        production_time = calculate_production_time(sample.avg_production_time, actual_production)

        new_stock = sample.stock_quantity + actual_production - order.quantity
        self._sample_repository.update_stock(sample.sample_id, new_stock)
        self._order_repository.update_status(order.order_no, CONFIRMED)

        return (
            f"생산 완료. 주문 '{order.order_no}' 실 생산량: {actual_production}ea "
            f"(생산시간 {production_time}분). 상태가 CONFIRMED로 전환되었습니다."
        )

    def list_production_queue(self) -> str:
        return format_order_table(self._order_repository.find_by_status(PRODUCING))
