from base import BaseModel


class Webhook(BaseModel):
    def __init__(
        self,
        data: dict,
    ) -> None:
        super().__init__(data, "topic")
