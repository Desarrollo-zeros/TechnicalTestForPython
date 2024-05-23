import unittest
import os
import pandas as pd
import sys

from app.domain.contracts.Idata_loader import IDataLoader
from app.domain.sales.sale import Sale
from app.infrastructure.data.data_frame_manager import DataFrameManager
from app.infrastructure.data.data_loader import DataLoader

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))


class TestDataFrameManager(unittest.TestCase):
    data_loader: IDataLoader = None

    def setUp(self):
        # Crear un directorio de prueba
        self.test_dir = 'test_data'
        os.makedirs(self.test_dir, exist_ok=True)

        # Crear un DataFrame de prueba
        self.df1 = pd.DataFrame({
            'KeySale': ['sale1', 'sale2'],
            'KeyDate': [pd.Timestamp('2023-01-01'), pd.Timestamp('2023-01-02')],
            'KeyStore': ['store1', 'store2'],
            'KeyWarehouse': ['warehouse1', 'warehouse2'],
            'KeyCustomer': ['customer1', 'customer2'],
            'KeyProduct': ['product1', 'product2'],
            'KeyEmployee': ['employee1', 'employee2'],
            'KeyCurrency': ['currency1', 'currency2'],
            'KeyDivision': ['division1', 'division2'],
            'KeyTicket': ['ticket1', 'ticket2'],
            'KeyCedi': ['cedi1', 'cedi2'],
            'TicketId': ['ticketid1', 'ticketid2'],
            'Qty': [1.0, 2.0],
            'Amount': [100.0, 200.0],
            'CostAmount': [50.0, 150.0],
            'DiscAmount': [5.0, 10.0],
            'Tickets': ['tickets1', 'tickets2'],
            'Products': ['products1', 'products2'],
            'Customers': ['customers1', 'customers2'],
            'Employees': ['employees1', 'employees2'],
            'Stores': ['stores1', 'stores2'],
            'Divisions': ['divisions1', 'divisions2'],
            'Time': ['time1', 'time2'],
            'Cedis': ['cedis1', 'cedis2']
        })

        self.df1.to_parquet(os.path.join(self.test_dir, 'test1.parquet'))
        self.data_loader = DataLoader()

    def tearDown(self):
        # Eliminar los archivos y el directorio de prueba después de cada prueba
        for f in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, f))
        os.rmdir(self.test_dir)

    def test_query_sales(self):
        # Crear una instancia de DataFrameManager con DataLoader inyectado

        df_manager = DataFrameManager(self.data_loader, self.test_dir)

        # Consultar los datos utilizando el modelo Sale
        sales = df_manager.query(Sale)
        self.assertEqual(len(sales), 2)
        self.assertIsInstance(sales[0], Sale)
        self.assertEqual(sales[0].KeySale, 'sale1')
        self.assertEqual(sales[1].KeySale, 'sale2')


if __name__ == '__main__':
    unittest.main()
