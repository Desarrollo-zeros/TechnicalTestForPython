from abc import ABC, abstractmethod
from datetime import date
from typing import List
from app.domain.entities.sales.sale import Sale
from app.domain.outputs.employee_sales_output import EmployeeSalesOutput
from app.domain.outputs.product_sales_output import ProductSalesOutput
from app.domain.outputs.store_sales_output import StoreSalesOutput


class ISaleService(ABC):

    @abstractmethod
    def get_sales_by_employee(self, key_employee: str, start_date: date, end_date: date) -> List[Sale]:
        pass

    @abstractmethod
    def get_sales_by_product(self, key_product: str, start_date: date, end_date: date) -> List[Sale]:
        pass

    @abstractmethod
    def get_sales_by_store(self, key_store: str, start_date: date, end_date: date) -> List[Sale]:
        pass

    @abstractmethod
    def get_total_avg_sales_by_store(self) -> List[StoreSalesOutput]:
        pass

    @abstractmethod
    def get_total_avg_sales_by_product(self) -> List[ProductSalesOutput]:
        pass

    @abstractmethod
    def get_total_avg_sales_by_employee(self) -> List[EmployeeSalesOutput]:
        pass
