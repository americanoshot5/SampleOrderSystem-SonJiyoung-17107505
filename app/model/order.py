from dataclasses import dataclass

from app.model.order_status import RESERVED


@dataclass
class Order:
    order_no: str
    sample_id: str
    customer_name: str
    quantity: int
    status: str = RESERVED
    created_at: str = ""
