from base import BaseModel


class Customer(BaseModel):
    def __init__(self, data: dict) -> None:
        super().__init__(data, "email_marketing_consent")
