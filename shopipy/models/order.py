from base import BaseModel


class Order(BaseModel):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
