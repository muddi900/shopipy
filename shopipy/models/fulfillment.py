from base import BaseModel


class Fullfilment(BaseModel):
    def __init__(self, data: dict) -> None:
        super().__init__(data, "tracking_numbers")
