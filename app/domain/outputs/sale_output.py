from datetime import datetime
from pydantic import BaseModel


class SaleOutput(BaseModel):
    KeySale: str
    KeyDate: datetime
    KeyStore: str
    KeyWarehouse: str
    KeyCustomer: str
    KeyProduct: str
    KeyEmployee: str
    KeyCurrency: str
    KeyDivision: str
    KeyTicket: str
    KeyCedi: str
    TicketId: str
    Qty: float
    Amount: float
    CostAmount: float
    DiscAmount: float
    Tickets: str
    Products: str
    Customers: str
    Employees: str
    Stores: str
    Divisions: str
    Time: str
    Cedis: str
