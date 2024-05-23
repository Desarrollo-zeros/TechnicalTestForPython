from pydantic import BaseModel
from datetime import datetime


class EmployeeInput(BaseModel):
    KeyEmployee: str
    StartDate: datetime
    EndDate: datetime
