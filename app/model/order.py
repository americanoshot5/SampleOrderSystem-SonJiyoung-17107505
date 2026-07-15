from dataclasses import dataclass


@dataclass
class Order:
    order_no: str
    sample_id: str
    customer_name: str
    quantity: int
    status: str = "RESERVED"
    created_at: str = ""
