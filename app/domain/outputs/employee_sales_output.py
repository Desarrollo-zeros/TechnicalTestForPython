from pydantic import BaseModel


class EmployeeSalesOutput(BaseModel):
    KeyEmployee: str
    total_sales: float
    avg_sales: float
