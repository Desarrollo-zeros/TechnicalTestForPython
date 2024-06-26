from datetime import date
from pydantic import BaseModel


class SaleOutput(BaseModel):
    KeySale: str
    KeyDate: date
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
    Tickets: dict
    Products: dict
    Customers: dict
    Employees: dict
    Stores: dict
    Divisions: dict
    Time: dict
    Cedis: dict
