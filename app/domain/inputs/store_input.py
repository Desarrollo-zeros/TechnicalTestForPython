from datetime import datetime
from pydantic import BaseModel


class StoreInput(BaseModel):
    KeyStore: str
    StartDate: datetime
    EndDate: datetime
