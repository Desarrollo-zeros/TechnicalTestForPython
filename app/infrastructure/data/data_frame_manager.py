from typing import Type, List, TypeVar, Optional

from app.domain.contracts.infrastructures.i_data_frame_manager import IDataFrameManager
from app.domain.contracts.infrastructures.i_data_loader import IDataLoader
from app.domain.base import BaseModel

T = TypeVar('T', bound=BaseModel)


class DataFrameManager(IDataFrameManager[T]):
    _instance: Optional['DataFrameManager'] = None

    def __new__(cls, data_loader: IDataLoader, data_directory: str):
        if cls._instance is None:
            cls._instance = super(DataFrameManager, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, data_loader: IDataLoader, data_directory: str):
        if self.__initialized:
            return
        self.data_loader = data_loader
        self.data_directory = data_directory
        self.dataframe = self.data_loader.load_parquet_files(data_directory)
        self.__initialized = True

    def query(self, model: Type[T]) -> List[T]:
        return model.from_dataframe(self.dataframe)
