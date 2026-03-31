from abc import ABC, abstractmethod
from contextlib import _AsyncGeneratorContextManager
from typing import AsyncIterator, Self


class ConsumerInterface(ABC):

    @property
    @abstractmethod
    def client(self) -> _AsyncGeneratorContextManager[Self]:
        pass

    @property
    @abstractmethod
    def messages(self) -> AsyncIterator[bytes]:
        pass
