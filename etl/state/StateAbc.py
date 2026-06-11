import abc
from typing import Any


class BaseState(abc.ABC):
    @abc.abstractmethod
    def set_state(self, key: str, value: Any) -> None:
        pass

    @abc.abstractmethod
    def get_state(self, key: str) -> Any:
        pass
