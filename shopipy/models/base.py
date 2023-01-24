from typing import Any
from abc import ABC


class BaseModel(ABC):
    """
    This is the base class. Due to the verbose nature of Shopify's json objects, having simple dict parse for the objects would save a lot of time.
    """

    def __init__(self, data: dict, test_field: str) -> None:

        if test_field not in data:
            raise AttributeError("The resource is incorrect for this model.")
        self.__data = data

    def __getattr__(self, __name: str) -> Any:
        return self.__data[__name]
