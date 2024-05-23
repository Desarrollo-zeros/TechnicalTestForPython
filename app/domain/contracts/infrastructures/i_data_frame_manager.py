from abc import ABC, abstractmethod
from typing import Type, List, TypeVar, Generic
from app.domain.base import BaseModel

T = TypeVar('T', bound=BaseModel)


class IDataFrameManager(ABC, Generic[T]):

    @abstractmethod
    def query(self, model: Type[T]) -> List[T]:
        pass
