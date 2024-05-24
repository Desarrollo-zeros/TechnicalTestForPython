import sys
import unittest
import os
import tempfile
import warnings

import pandas as pd
from datetime import datetime
from cachetools import TTLCache
from app.domain.contracts.services.i_sale_service import ISaleService
from app.domain.entities.sales.sale import Sale
from app.infrastructure.data.data_loader import DataLoader
from app.infrastructure.data.data_frame_manager import DataFrameManager
from app.services.sale_service import SaleService

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

class TestSaleService(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()

        self.df1 = pd.DataFrame({
            'KeySale': ['sale1', 'sale2', 'sale3'],
            'KeyDate': [pd.Timestamp('2023-01-01').date(), pd.Timestamp('2023-01-02').date(), pd.Timestamp('2023-01-03').date()],
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

        self.df1.to_parquet(os.path.join(self.test_dir.name, 'test1.parquet'))
        cache = TTLCache(maxsize=1, ttl=360)
        data_loader = DataLoader(cache)
        data_manager = DataFrameManager(data_loader, self.test_dir.name)
        self.sale_service: ISaleService = SaleService(data_manager)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_get_sales_by_employee(self):
        sales = self.sale_service.get_sales_by_employee('employee1', datetime(2023, 1, 1).date(), datetime(2023, 1, 3).date())
        sale: Sale  = sales[0]
        self.assertEqual(len(sales), 1)
        self.assertEqual(sales[0].KeySale, 'sale1')


    def test_get_sales_by_product(self):
        sales = self.sale_service.get_sales_by_product('product1', datetime(2023, 1, 1).date(), datetime(2023, 1, 3).date())
        self.assertEqual(len(sales), 1)
        self.assertEqual(sales[0].KeySale, 'sale1')


    def test_get_sales_by_store(self):
        sales = self.sale_service.get_sales_by_store('store1', datetime(2023, 1, 1).date(), datetime(2023, 1, 3).date())
        self.assertEqual(len(sales), 1)
        self.assertEqual(sales[0].KeySale, 'sale1')

    def test_get_total_avg_sales_by_store(self):
        result = self.sale_service.get_total_avg_sales_by_store()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].KeyStore, 'store1')
        self.assertAlmostEqual(result[0].total_sales, 100.0)
        self.assertAlmostEqual(result[0].avg_sales, 100.0)

    def test_get_total_avg_sales_by_product(self):
        result = self.sale_service.get_total_avg_sales_by_product()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].KeyProduct, 'product1')
        self.assertAlmostEqual(result[0].total_sales, 100.0)
        self.assertAlmostEqual(result[0].avg_sales, 100.0)

    def test_get_total_avg_sales_by_employee(self):
        result = self.sale_service.get_total_avg_sales_by_employee()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].KeyEmployee, 'employee1')
        self.assertAlmostEqual(result[0].total_sales, 100.0)
        self.assertAlmostEqual(result[0].avg_sales, 100.0)

if __name__ == '__main__':
    unittest.main()
