from pydantic import BaseModel


class ProductSalesOutput(BaseModel):
    KeyProduct: str
    total_sales: float
    avg_sales: float
