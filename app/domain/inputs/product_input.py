from datetime import datetime
from pydantic import BaseModel


class ProductInput(BaseModel):
    KeyProduct: str
    ProductName: str
    ProductCategory: str
    ProductPrice: float
    ProductStock: int
    CreatedAt: datetime
