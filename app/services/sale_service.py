from typing import List
from datetime import datetime
import pandas as pd

from app.domain.contracts.infrastructures.i_data_frame_manager import IDataFrameManager
from app.domain.entities.sales.sale import Sale
from app.domain.contracts.services.i_sale_service import ISaleService


class SaleService(ISaleService):
    def __init__(self, data_manager: IDataFrameManager):
        self.data_manager = data_manager

    def get_sales_by_employee(self, key_employee: str, start_date: datetime, end_date: datetime) -> List[Sale]:
        sales = self.data_manager.query(Sale)
        return [sale for sale in sales if sale.KeyEmployee == key_employee and start_date <= sale.KeyDate <= end_date]

    def get_sales_by_product(self, key_product: str, start_date: datetime, end_date: datetime) -> List[Sale]:
        sales = self.data_manager.query(Sale)
        return [sale for sale in sales if sale.KeyProduct == key_product and start_date <= sale.KeyDate <= end_date]

    def get_sales_by_store(self, key_store: str, start_date: datetime, end_date: datetime) -> List[Sale]:
        sales = self.data_manager.query(Sale)
        return [sale for sale in sales if sale.KeyStore == key_store and start_date <= sale.KeyDate <= end_date]

    def get_total_avg_sales_by_store(self) -> List[dict]:
        sales = self.data_manager.query(Sale)
        df = pd.DataFrame([sale.__dict__ for sale in sales])
        return df.groupby("KeyStore").agg(total_sales=pd.NamedAgg(column="Amount", aggfunc="sum"),
                                          avg_sales=pd.NamedAgg(column="Amount", aggfunc="mean")).reset_index().to_dict(
            orient="records")

    def get_total_avg_sales_by_product(self) -> List[dict]:
        sales = self.data_manager.query(Sale)
        df = pd.DataFrame([sale.__dict__ for sale in sales])
        return df.groupby("KeyProduct").agg(total_sales=pd.NamedAgg(column="Amount", aggfunc="sum"),
                                            avg_sales=pd.NamedAgg(column="Amount",
                                                                  aggfunc="mean")).reset_index().to_dict(
            orient="records")

    def get_total_avg_sales_by_employee(self) -> List[dict]:
        sales = self.data_manager.query(Sale)
        df = pd.DataFrame([sale.__dict__ for sale in sales])
        return df.groupby("KeyEmployee").agg(total_sales=pd.NamedAgg(column="Amount", aggfunc="sum"),
                                             avg_sales=pd.NamedAgg(column="Amount",
                                                                   aggfunc="mean")).reset_index().to_dict(
            orient="records")
