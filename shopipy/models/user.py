from base import BaseModel


class User(BaseModel):
    def __init__(self, data: dict) -> None:
        super().__init__(data, "email_marketing_consent")
