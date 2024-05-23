from datetime import datetime
from pydantic import BaseModel


class StoreOutput(BaseModel):
    KeyStore: str
    StoreName: str
    StoreLocation: str
    CreatedAt: datetime
