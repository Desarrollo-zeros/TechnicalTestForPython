from typing import List
from datetime import datetime

import pandas as pd

from app.domain.contracts.infrastructures.Idata_loader import IDataLoader
from app.infrastructure.data.data_frame_manager import DataFrameManager
from app.domain.sales.sale import Sale
from app.infrastructure.data.data_loader import DataLoader

class SaleService:
    def __init__(self, data_directory: str):
        data_loader: IDataLoader = DataLoader()
        self.data_manager = DataFrameManager(data_loader, data_directory)

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
                                          avg_sales=pd.NamedAgg(column="Amount", aggfunc="mean")).reset_index().to_dict(orient="records")

    def get_total_avg_sales_by_product(self) -> List[dict]:
        sales = self.data_manager.query(Sale)
        df = pd.DataFrame([sale.__dict__ for sale in sales])
        return df.groupby("KeyProduct").agg(total_sales=pd.NamedAgg(column="Amount", aggfunc="sum"),
                                            avg_sales=pd.NamedAgg(column="Amount", aggfunc="mean")).reset_index().to_dict(orient="records")

    def get_total_avg_sales_by_employee(self) -> List[dict]:
        sales = self.data_manager.query(Sale)
        df = pd.DataFrame([sale.__dict__ for sale in sales])
        return df.groupby("KeyEmployee").agg(total_sales=pd.NamedAgg(column="Amount", aggfunc="sum"),
                                             avg_sales=pd.NamedAgg(column="Amount", aggfunc="mean")).reset_index().to_dict(orient="records")
