from base import BaseModel


class Product(BaseModel):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
