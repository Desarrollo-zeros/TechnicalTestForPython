from abc import ABC, abstractmethod
from typing import List
from datetime import datetime
from app.domain.entities.sales.sale import Sale


class ISaleService(ABC):

    @abstractmethod
    def get_sales_by_employee(self, key_employee: str, start_date: datetime, end_date: datetime) -> List[Sale]:
        pass

    @abstractmethod
    def get_sales_by_product(self, key_product: str, start_date: datetime, end_date: datetime) -> List[Sale]:
        pass

    @abstractmethod
    def get_sales_by_store(self, key_store: str, start_date: datetime, end_date: datetime) -> List[Sale]:
        pass

    @abstractmethod
    def get_total_avg_sales_by_store(self) -> List[dict]:
        pass

    @abstractmethod
    def get_total_avg_sales_by_product(self) -> List[dict]:
        pass

    @abstractmethod
    def get_total_avg_sales_by_employee(self) -> List[dict]:
        pass
