from typing import List
from datetime import datetime
import pandas as pd
from tqdm import tqdm

from app.domain.contracts.infrastructures.i_data_frame_manager import IDataFrameManager
from app.domain.entities.sales.sale import Sale
from app.domain.contracts.services.i_sale_service import ISaleService
from app.domain.outputs.employee_sales_output import EmployeeSalesOutput
from app.domain.outputs.product_sales_output import ProductSalesOutput
from app.domain.outputs.store_sales_output import StoreSalesOutput
from app.infrastructure.data.data_loader import DataLoader, cached_property
from app.core.config import settings


class SaleService(ISaleService):
    def __init__(self, data_manager: IDataFrameManager):
        self.data_manager = data_manager

    @cached_property
    def get_sales_dataframe(self) -> pd.DataFrame:
        sales = self.data_manager.query(Sale)
        return pd.DataFrame([sale.__dict__ for sale in tqdm(sales, desc="Cargando datos", unit="registros")])

    def get_sales_by_employee(self, key_employee: str, start_date: datetime, end_date: datetime) -> List[Sale]:
        df = self.get_sales_dataframe()
        filtered_df = df[(df['KeyEmployee'] == key_employee) & (df['KeyDate'] >= start_date) & (df['KeyDate'] <= end_date)]
        return filtered_df.to_dict(orient='records')

    def get_sales_by_product(self, key_product: str, start_date: datetime, end_date: datetime) -> List[Sale]:
        df = self.get_sales_dataframe()
        filtered_df = df[(df['KeyProduct'] == key_product) & (df['KeyDate'] >= start_date) & (df['KeyDate'] <= end_date)]
        return filtered_df.to_dict(orient='records')

    def get_sales_by_store(self, key_store: str, start_date: datetime, end_date: datetime) -> List[Sale]:
        df = self.get_sales_dataframe()
        filtered_df = df[(df['KeyStore'] == key_store) & (df['KeyDate'] >= start_date) & (df['KeyDate'] <= end_date)]
        return filtered_df.to_dict(orient='records')

    def get_total_avg_sales_by_store(self) -> List[StoreSalesOutput]:
        df = self.get_sales_dataframe()
        result = df.groupby("KeyStore").agg(total_sales=pd.NamedAgg(column="Amount", aggfunc="sum"),
                                            avg_sales=pd.NamedAgg(column="Amount", aggfunc="mean")).reset_index().to_dict(
            orient="records")
        return [StoreSalesOutput(**item) for item in result]

    def get_total_avg_sales_by_product(self) -> List[ProductSalesOutput]:
        df = self.get_sales_dataframe()
        result = df.groupby("KeyProduct").agg(total_sales=pd.NamedAgg(column="Amount", aggfunc="sum"),
                                              avg_sales=pd.NamedAgg(column="Amount", aggfunc="mean")).reset_index().to_dict(
            orient="records")
        return [ProductSalesOutput(**item) for item in result]

    def get_total_avg_sales_by_employee(self) -> List[EmployeeSalesOutput]:
        df = self.get_sales_dataframe()
        result = df.groupby("KeyEmployee").agg(total_sales=pd.NamedAgg(column="Amount", aggfunc="sum"),
                                               avg_sales=pd.NamedAgg(column="Amount", aggfunc="mean")).reset_index().to_dict(
            orient="records")
        return [EmployeeSalesOutput(**item) for item in result]
