from pydantic import BaseModel


class StoreSalesOutput(BaseModel):
    KeyStore: str
    total_sales: float
    avg_sales: float
