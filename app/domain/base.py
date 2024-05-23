from typing import TypeVar, Type, List, Any
import pandas as pd

T = TypeVar('T', bound='BaseModel')


class BaseModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_dataframe(cls: Type[T], df: pd.DataFrame) -> List[T]:
        records = df.to_dict(orient='records')
        return [cls(**record) for record in records]
