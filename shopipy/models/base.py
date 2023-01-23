from typing import Any
from abc import ABC


class BaseModel(ABC):
    def __init__(self, data: dict) -> None:
        self.__data = data

    def __getattr__(self, __name: str) -> Any:
        return self.__data[__name]
