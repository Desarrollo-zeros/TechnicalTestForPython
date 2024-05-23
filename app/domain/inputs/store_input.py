from datetime import datetime
from pydantic import BaseModel


class StoreInput(BaseModel):
    KeyStore: str
    StoreName: str
    StoreLocation: str
    CreatedAt: datetime
