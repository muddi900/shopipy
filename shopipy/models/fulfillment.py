from base import BaseModel


class Fulfillment(BaseModel):
    def __init__(self, data: dict) -> None:
        super().__init__(data, "tracking_numbers")
