from typing import Type, List, TypeVar

from app.domain.contracts.infrastructures.i_data_frame_manager import IDataFrameManager
from app.domain.contracts.infrastructures.i_data_loader import IDataLoader
from app.domain.base import BaseModel

T = TypeVar('T', bound=BaseModel)


class DataFrameManager(IDataFrameManager[T]):
    def __init__(self, data_loader: IDataLoader, data_directory: str):
        self.data_loader = data_loader
        self.data_directory = data_directory
        self.dataframe = self.data_loader.load_parquet_files(data_directory)

    def query(self, model: Type[T]) -> List[T]:
        return model.from_dataframe(self.dataframe)
