import unittest
import os
import pandas as pd
from datetime import datetime

from cachetools import TTLCache

from app.infrastructure.data.data_loader import DataLoader
from app.infrastructure.data.data_frame_manager import DataFrameManager
from app.services.sale_service import SaleService


class TestSaleService(unittest.TestCase):

    def setUp(self):
        # Crear un directorio de prueba
        self.test_dir = 'test_data'
        os.makedirs(self.test_dir, exist_ok=True)

        # Crear un DataFrame de prueba
        self.df1 = pd.DataFrame({
            'KeySale': ['sale1', 'sale2', 'sale3'],
            'KeyDate': [pd.Timestamp('2023-01-01'), pd.Timestamp('2023-01-02'), pd.Timestamp('2023-01-03')],
            'KeyStore': ['store1', 'store2', 'store1'],
            'KeyWarehouse': ['warehouse1', 'warehouse2', 'warehouse1'],
            'KeyCustomer': ['customer1', 'customer2', 'customer1'],
            'KeyProduct': ['product1', 'product2', 'product1'],
            'KeyEmployee': ['employee1', 'employee2', 'employee1'],
            'KeyCurrency': ['currency1', 'currency2', 'currency1'],
            'KeyDivision': ['division1', 'division2', 'division1'],
            'KeyTicket': ['ticket1', 'ticket2', 'ticket3'],
            'KeyCedi': ['cedi1', 'cedi2', 'cedi1'],
            'TicketId': ['ticketid1', 'ticketid2', 'ticketid3'],
            'Qty': [1.0, 2.0, 1.0],
            'Amount': [100.0, 200.0, 150.0],
            'CostAmount': [50.0, 150.0, 75.0],
            'DiscAmount': [5.0, 10.0, 7.5],
            'Tickets': ['tickets1', 'tickets2', 'tickets3'],
            'Products': ['products1', 'products2', 'products3'],
            'Customers': ['customers1', 'customers2', 'customers3'],
            'Employees': ['employees1', 'employees2', 'employees3'],
            'Stores': ['stores1', 'stores2', 'stores3'],
            'Divisions': ['divisions1', 'divisions2', 'divisions3'],
            'Time': ['time1', 'time2', 'time3'],
            'Cedis': ['cedis1', 'cedis2', 'cedis3']
        })

        self.df1.to_parquet(os.path.join(self.test_dir, 'test1.parquet'))
        cache = TTLCache(maxsize=1, ttl=360)
        data_loader = DataLoader(cache)
        data_manager = DataFrameManager(data_loader, self.test_dir)
        self.sale_service = SaleService(data_manager)

    def tearDown(self):
        # Eliminar los archivos y el directorio de prueba después de cada prueba
        for f in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, f))
        os.rmdir(self.test_dir)

    def test_get_sales_by_employee(self):
        # Probar la obtención de ventas por empleado
        sales = self.sale_service.get_sales_by_employee('employee1', datetime(2023, 1, 1), datetime(2023, 1, 3))
        self.assertEqual(len(sales), 2)
        self.assertEqual(sales[0].KeySale, 'sale1')
        self.assertEqual(sales[1].KeySale, 'sale3')

    def test_get_sales_by_product(self):
        # Probar la obtención de ventas por producto
        sales = self.sale_service.get_sales_by_product('product1', datetime(2023, 1, 1), datetime(2023, 1, 3))
        self.assertEqual(len(sales), 2)
        self.assertEqual(sales[0].KeySale, 'sale1')
        self.assertEqual(sales[1].KeySale, 'sale3')

    def test_get_sales_by_store(self):
        # Probar la obtención de ventas por tienda
        sales = self.sale_service.get_sales_by_store('store1', datetime(2023, 1, 1), datetime(2023, 1, 3))
        self.assertEqual(len(sales), 2)
        self.assertEqual(sales[0].KeySale, 'sale1')
        self.assertEqual(sales[1].KeySale, 'sale3')

    def test_get_total_avg_sales_by_store(self):
        # Probar la obtención de ventas totales y promedio por tienda
        result = self.sale_service.get_total_avg_sales_by_store()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['KeyStore'], 'store1')
        self.assertEqual(result[0]['total_sales'], 250.0)
        self.assertEqual(result[0]['avg_sales'], 125.0)

    def test_get_total_avg_sales_by_product(self):
        # Probar la obtención de ventas totales y promedio por producto
        result = self.sale_service.get_total_avg_sales_by_product()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['KeyProduct'], 'product1')
        self.assertEqual(result[0]['total_sales'], 250.0)
        self.assertEqual(result[0]['avg_sales'], 125.0)

    def test_get_total_avg_sales_by_employee(self):
        # Probar la obtención de ventas totales y promedio por empleado
        result = self.sale_service.get_total_avg_sales_by_employee()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['KeyEmployee'], 'employee1')
        self.assertEqual(result[0]['total_sales'], 250.0)
        self.assertEqual(result[0]['avg_sales'], 125.0)


if __name__ == '__main__':
    unittest.main()
