from abc import ABC, abstractmethod
import pandas as pd


class IDataLoader(ABC):

    def __init__(self):
        self._load_thread = None

    @abstractmethod
    def load_parquet_files(self, directory: str) -> pd.DataFrame:
        pass
