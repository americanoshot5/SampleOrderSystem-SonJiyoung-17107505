from app.model.order_repository import OrderRepository
from app.model.sample_repository import SampleRepository

ORDER_STATUSES = ["RESERVED", "CONFIRMED", "PRODUCING", "RELEASE"]


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
