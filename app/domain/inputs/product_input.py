from datetime import datetime
from pydantic import BaseModel


class ProductInput(BaseModel):
    KeyProduct: str
    StartDate: datetime
    EndDate: datetime
