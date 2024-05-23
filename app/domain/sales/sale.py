from datetime import datetime
from app.domain.base import BaseModel


class Sale(BaseModel):
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

    def __init__(self, KeySale: str, KeyDate: datetime, KeyStore: str, KeyWarehouse: str, KeyCustomer: str,
                 KeyProduct: str, KeyEmployee: str, KeyCurrency: str, KeyDivision: str, KeyTicket: str,
                 KeyCedi: str, TicketId: str, Qty: float, Amount: float, CostAmount: float, DiscAmount: float,
                 Tickets: str, Products: str, Customers: str, Employees: str, Stores: str, Divisions: str,
                 Time: str, Cedis: str):
        super().__init__(KeySale=KeySale, KeyDate=KeyDate, KeyStore=KeyStore, KeyWarehouse=KeyWarehouse,
                         KeyCustomer=KeyCustomer, KeyProduct=KeyProduct, KeyEmployee=KeyEmployee,
                         KeyCurrency=KeyCurrency, KeyDivision=KeyDivision, KeyTicket=KeyTicket, KeyCedi=KeyCedi,
                         TicketId=TicketId, Qty=Qty, Amount=Amount, CostAmount=CostAmount, DiscAmount=DiscAmount,
                         Tickets=Tickets, Products=Products, Customers=Customers, Employees=Employees,
                         Stores=Stores, Divisions=Divisions, Time=Time, Cedis=Cedis)
