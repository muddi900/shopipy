from dataclasses import dataclass


@dataclass
class Fulfillment:
    created_at: str
    id: int
    order_id: int
    status: str
    tracking_company: str
    tracking_number: str
    updated_at: str
