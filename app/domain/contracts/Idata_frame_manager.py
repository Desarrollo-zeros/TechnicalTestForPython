from abc import ABC, abstractmethod
from typing import Type, List
from app.domain.base import BaseModel


class IDataFrameManager(ABC):

    @abstractmethod
    def query(self, model: Type[BaseModel]) -> List[BaseModel]:
        pass
