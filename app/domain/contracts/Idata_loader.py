from abc import ABC, abstractmethod
import pandas as pd


class IDataLoader(ABC):

    @abstractmethod
    def load_parquet_files(self, directory: str) -> pd.DataFrame:
        pass
