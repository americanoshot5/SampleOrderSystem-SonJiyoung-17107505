from app.model.order_repository import OrderRepository
from app.model.sample_repository import SampleRepository
from app.model.stock_status import determine_stock_status

ORDER_STATUSES = ["RESERVED", "CONFIRMED", "PRODUCING", "RELEASE"]
PENDING_ORDER_STATUSES = ("RESERVED", "PRODUCING")


class MonitoringController:
    def __init__(self, order_repository: OrderRepository, sample_repository: SampleRepository):
        self._order_repository = order_repository
        self._sample_repository = sample_repository

    def summarize_order_status(self) -> str:
        lines = [
            f"{status}: {len(self._order_repository.find_by_status(status))}"
            for status in ORDER_STATUSES
        ]
        return "\n".join(lines)

    def summarize_stock_status(self) -> str:
        orders = self._order_repository.find_all()
        lines = []
        for sample in self._sample_repository.find_all():
            pending = sum(
                order.quantity
                for order in orders
                if order.sample_id == sample.sample_id and order.status in PENDING_ORDER_STATUSES
            )
            status = determine_stock_status(sample.stock_quantity, pending)
            lines.append(f"{sample.sample_id} {sample.name} 재고:{sample.stock_quantity} 상태:{status}")
        return "\n".join(lines)
