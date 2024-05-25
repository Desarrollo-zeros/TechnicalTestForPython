from typing import List
from datetime import date
import pandas as pd
from tqdm import tqdm

from app.domain.contracts.infrastructures.i_data_frame_manager import IDataFrameManager
from app.domain.entities.sales.sale import Sale
from app.domain.contracts.services.i_sale_service import ISaleService
from app.domain.outputs.employee_sales_output import EmployeeSalesOutput
from app.domain.outputs.product_sales_output import ProductSalesOutput
from app.domain.outputs.store_sales_output import StoreSalesOutput
from app.infrastructure.data.data_loader import cached_property


class SaleService(ISaleService):
    """
    Servicio para gestionar las ventas.

    :param data_manager: Instancia de IDataFrameManager para manejar la gestión de datos.
    """

    def __init__(self, data_manager: IDataFrameManager):
        self.data_manager = data_manager

    @cached_property
    def get_sales_dataframe(self) -> pd.DataFrame:
        """
        Obtiene un DataFrame con todas las ventas.

        :return: DataFrame con los datos de ventas.
        """
        sales = self.data_manager.query(Sale)
        df = pd.DataFrame([sale.__dict__ for sale in tqdm(sales, desc="Cargando datos", unit="registros")])
        df['KeyDate'] = pd.to_datetime(df['KeyDate']).dt.date
        return df

    def paginate(self, df: pd.DataFrame, page: int = 1, page_size: int = 10) -> pd.DataFrame:
        """
        Pagina un DataFrame.

        :param df: DataFrame a paginar.
        :param page: Número de página. Valor por defecto: 1.
        :param page_size: Tamaño de la página. Valor por defecto: 10.
        :return: DataFrame paginado.
        """
        start = (page - 1) * page_size
        end = start + page_size
        return df.iloc[start:end]

    def get_sales_by_employee(self, key_employee: str, start_date: date, end_date: date, page: int = 1, page_size: int = 10) \
            -> List[Sale]:
        """
        Obtiene las ventas por empleado en un periodo de tiempo con paginación.

        :param key_employee: Clave del empleado.
        :param start_date: Fecha de inicio.
        :param end_date: Fecha de fin.
        :param page: Número de página. Valor por defecto: 1.
        :param page_size: Tamaño de la página. Valor por defecto: 10.
        :return: Lista de ventas.
        """
        df = self.get_sales_dataframe()
        filtered_df = df[(df['KeyEmployee'] == key_employee) & (df['KeyDate'] >= start_date) & (df['KeyDate'] <= end_date)]
        paginated_df = self.paginate(filtered_df, page, page_size)
        return [Sale(**item) for item in paginated_df.to_dict(orient='records')]

    def get_sales_by_product(self, key_product: str, start_date: date, end_date: date, page: int = 1, page_size: int = 10) \
            -> List[Sale]:
        """
        Obtiene las ventas por producto en un periodo de tiempo con paginación.

        :param key_product: Clave del producto.
        :param start_date: Fecha de inicio.
        :param end_date: Fecha de fin.
        :param page: Número de página. Valor por defecto: 1.
        :param page_size: Tamaño de la página. Valor por defecto: 10.
        :return: Lista de ventas.
        """
        df = self.get_sales_dataframe()
        filtered_df = df[(df['KeyProduct'] == key_product) & (df['KeyDate'] >= start_date) & (df['KeyDate'] <= end_date)]
        paginated_df = self.paginate(filtered_df, page, page_size)
        return [Sale(**item) for item in paginated_df.to_dict(orient='records')]

    def get_sales_by_store(self, key_store: str, start_date: date, end_date: date, page: int = 1, page_size: int = 10) \
            -> List[Sale]:
        """
        Obtiene las ventas por tienda en un periodo de tiempo con paginación.

        :param key_store: Clave de la tienda.
        :param start_date: Fecha de inicio.
        :param end_date: Fecha de fin.
        :param page: Número de página. Valor por defecto: 1.
        :param page_size: Tamaño de la página. Valor por defecto: 10.
        :return: Lista de ventas.
        """
        df = self.get_sales_dataframe()
        filtered_df = df[(df['KeyStore'] == key_store) & (df['KeyDate'] >= start_date) & (df['KeyDate'] <= end_date)]
        paginated_df = self.paginate(filtered_df, page, page_size)
        return [Sale(**item) for item in paginated_df.to_dict(orient='records')]

    def get_total_avg_sales_by_store(self, page: int = 1, page_size: int = 10) -> List[StoreSalesOutput]:
        """
        Obtiene la venta total y promedio por tienda con paginación.

        :param page: Número de página. Valor por defecto: 1.
        :param page_size: Tamaño de la página. Valor por defecto: 10.
        :return: Lista de ventas totales y promedio por tienda.
        """
        df = self.get_sales_dataframe()
        result = df.groupby("KeyStore").agg(total_sales=pd.NamedAgg(column="Amount", aggfunc="sum"),
                                            avg_sales=pd.NamedAgg(column="Amount", aggfunc="mean")).reset_index()
        paginated_result = self.paginate(result, page, page_size).to_dict(orient="records")
        return [StoreSalesOutput(**item) for item in paginated_result]

    def get_total_avg_sales_by_product(self, page: int = 1, page_size: int = 10) -> List[ProductSalesOutput]:
        """
        Obtiene la venta total y promedio por producto con paginación.

        :param page: Número de página. Valor por defecto: 1.
        :param page_size: Tamaño de la página. Valor por defecto: 10.
        :return: Lista de ventas totales y promedio por producto.
        """
        df = self.get_sales_dataframe()
        result = df.groupby("KeyProduct").agg(total_sales=pd.NamedAgg(column="Amount", aggfunc="sum"),
                                              avg_sales=pd.NamedAgg(column="Amount", aggfunc="mean")).reset_index()
        paginated_result = self.paginate(result, page, page_size).to_dict(orient="records")
        return [ProductSalesOutput(**item) for item in paginated_result]

    def get_total_avg_sales_by_employee(self, page: int = 1, page_size: int = 10) -> List[EmployeeSalesOutput]:
        """
        Obtiene la venta total y promedio por empleado con paginación.

        :param page: Número de página. Valor por defecto: 1.
        :param page_size: Tamaño de la página. Valor por defecto: 10.
        :return: Lista de ventas totales y promedio por empleado.
        """
        df = self.get_sales_dataframe()
        result = df.groupby("KeyEmployee").agg(total_sales=pd.NamedAgg(column="Amount", aggfunc="sum"),
                                               avg_sales=pd.NamedAgg(column="Amount", aggfunc="mean")).reset_index()
        paginated_result = self.paginate(result, page, page_size).to_dict(orient="records")
        return [EmployeeSalesOutput(**item) for item in paginated_result]
