import unittest
from unittest.mock import patch
import pandas as pd
from fastapi.testclient import TestClient
from datetime import datetime
from app.core.config import settings
from app.main import app
from app.domain.contracts.infrastructures.i_data_frame_manager import IDataFrameManager
from app.domain.contracts.infrastructures.i_data_loader import IDataLoader
from app.domain.contracts.services.i_sale_service import ISaleService
from app.infrastructure.data.data_frame_manager import DataFrameManager
from app.domain.outputs.sale_output import SaleOutput
from app.domain.outputs.store_sales_output import StoreSalesOutput
from app.domain.outputs.product_sales_output import ProductSalesOutput
from app.domain.outputs.employee_sales_output import EmployeeSalesOutput
from app.services.sale_service import SaleService

client = TestClient(app)

def generate_mock_sales_data():
    data = {
        'KeySale': ['sale1', 'sale2', 'sale3'],
        'KeyDate': [datetime(2023, 1, 1).date(), datetime(2023, 1, 2).date(), datetime(2023, 1, 3).date()],
        'KeyStore': ['1|023', '1|007', '1|098'],
        'KeyWarehouse': ['warehouse1', 'warehouse2', 'warehouse3'],
        'KeyCustomer': ['customer1', 'customer2', 'customer3'],
        'KeyProduct': ['1|44733', '1|61889', '1|42606'],
        'KeyEmployee': ['1|343', '1|417', '1|569'],
        'KeyCurrency': ['currency1', 'currency2', 'currency3'],
        'KeyDivision': ['division1', 'division2', 'division3'],
        'KeyTicket': ['ticket1', 'ticket2', 'ticket3'],
        'KeyCedi': ['cedi1', 'cedi2', 'cedi3'],
        'TicketId': ['ticketid1', 'ticketid2', 'ticketid3'],
        'Qty': [1.0, 2.0, 3.0],
        'Amount': [100.0, 200.0, 300.0],
        'CostAmount': [50.0, 100.0, 150.0],
        'DiscAmount': [5.0, 10.0, 15.0],
        'Tickets': [{'example_key': 'example_value'}] * 3,
        'Products': [{'example_key': 'example_value'}] * 3,
        'Customers': [{'example_key': 'example_value'}] * 3,
        'Employees': [{'example_key': 'example_value'}] * 3,
        'Stores': [{'example_key': 'example_value'}] * 3,
        'Divisions': [{'example_key': 'example_value'}] * 3,
        'Time': [{'example_key': 'example_value'}] * 3,
        'Cedis': [{'example_key': 'example_value'}] * 3,
    }
    return pd.DataFrame(data)

class MockDataLoader(IDataLoader):
    def load_parquet_files(self, directory: str) -> pd.DataFrame:
        return generate_mock_sales_data()

def create_mock_sale_service() -> ISaleService:
    data_loader: IDataLoader = MockDataLoader()
    data_manager: IDataFrameManager = DataFrameManager(data_loader, "")
    sale_service: ISaleService = SaleService(data_manager)
    return sale_service

class TestSalesEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configurar el sale_service en el estado de la aplicación para pruebas
        settings.ml_models["sale_service"] = create_mock_sale_service()

    @patch("app.api.endpoints.sales.get_sale_service")
    def test_get_sales_by_employee(self, mock_get_sale_service):
        # Crear datos de ejemplo
        mock_service = mock_get_sale_service.return_value
        mock_service.get_sales_by_employee.return_value = [
            SaleOutput(
                KeySale="example_key_sale",
                KeyDate=datetime(2023, 1, 1).date(),
                KeyStore="example_key_store",
                KeyWarehouse="example_key_warehouse",
                KeyCustomer="example_key_customer",
                KeyProduct="example_key_product",
                KeyEmployee="example_key_employee",
                KeyCurrency="example_key_currency",
                KeyDivision="example_key_division",
                KeyTicket="example_key_ticket",
                KeyCedi="example_key_cedi",
                TicketId="example_ticket_id",
                Qty=1.0,
                Amount=100.0,
                CostAmount=50.0,
                DiscAmount=5.0,
                Tickets={"example_key": "example_value"},
                Products={"example_key": "example_value"},
                Customers={"example_key": "example_value"},
                Employees={"example_key": "example_value"},
                Stores={"example_key": "example_value"},
                Divisions={"example_key": "example_value"},
                Time={"example_key": "example_value"},
                Cedis={"example_key": "example_value"}
            )
        ]

        input_data = {
            "KeyEmployee": "1|343",
            "StartDate": "2023-01-01T00:00:00",
            "EndDate": "2023-12-31T23:59:59"
        }
        response = client.post("/api/v1/sales/employee", json=input_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 1)

    @patch("app.api.endpoints.sales.get_sale_service")
    def test_get_sales_by_product(self, mock_get_sale_service):
        mock_service = mock_get_sale_service.return_value
        mock_service.get_sales_by_product.return_value = [
            SaleOutput(
                KeySale="example_key_sale",
                KeyDate=datetime(2023, 1, 1).date(),
                KeyStore="example_key_store",
                KeyWarehouse="example_key_warehouse",
                KeyCustomer="example_key_customer",
                KeyProduct="example_key_product",
                KeyEmployee="example_key_employee",
                KeyCurrency="example_key_currency",
                KeyDivision="example_key_division",
                KeyTicket="example_key_ticket",
                KeyCedi="example_key_cedi",
                TicketId="example_ticket_id",
                Qty=1.0,
                Amount=100.0,
                CostAmount=50.0,
                DiscAmount=5.0,
                Tickets={"example_key": "example_value"},
                Products={"example_key": "example_value"},
                Customers={"example_key": "example_value"},
                Employees={"example_key": "example_value"},
                Stores={"example_key": "example_value"},
                Divisions={"example_key": "example_value"},
                Time={"example_key": "example_value"},
                Cedis={"example_key": "example_value"}
            )
        ]

        input_data = {
            "KeyProduct": "1|44733",
            "StartDate": "2023-01-01T00:00:00",
            "EndDate": "2023-12-31T23:59:59"
        }
        response = client.post("/api/v1/sales/product", json=input_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 1)

    @patch("app.api.endpoints.sales.get_sale_service")
    def test_get_sales_by_store(self, mock_get_sale_service):
        mock_service = mock_get_sale_service.return_value
        mock_service.get_sales_by_store.return_value = [
            SaleOutput(
                KeySale="example_key_sale",
                KeyDate=datetime(2023, 1, 1).date(),
                KeyStore="example_key_store",
                KeyWarehouse="example_key_warehouse",
                KeyCustomer="example_key_customer",
                KeyProduct="example_key_product",
                KeyEmployee="example_key_employee",
                KeyCurrency="example_key_currency",
                KeyDivision="example_key_division",
                KeyTicket="example_key_ticket",
                KeyCedi="example_key_cedi",
                TicketId="example_ticket_id",
                Qty=1.0,
                Amount=100.0,
                CostAmount=50.0,
                DiscAmount=5.0,
                Tickets={"example_key": "example_value"},
                Products={"example_key": "example_value"},
                Customers={"example_key": "example_value"},
                Employees={"example_key": "example_value"},
                Stores={"example_key": "example_value"},
                Divisions={"example_key": "example_value"},
                Time={"example_key": "example_value"},
                Cedis={"example_key": "example_value"}
            )
        ]

        input_data = {
            "KeyStore": "1|023",
            "StartDate": "2023-01-01T00:00:00",
            "EndDate": "2023-12-31T23:59:59"
        }
        response = client.post("/api/v1/sales/store", json=input_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 1)

    @patch("app.api.endpoints.sales.get_sale_service")
    def test_get_total_avg_sales_by_store(self, mock_get_sale_service):
        mock_service = mock_get_sale_service.return_value
        mock_service.get_total_avg_sales_by_store.return_value = [
            StoreSalesOutput(KeyStore="1|002", total_sales=1000.0, avg_sales=100.0)
        ]

        response = client.get("/api/v1/sales/store/total_avg")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 3)

    @patch("app.api.endpoints.sales.get_sale_service")
    def test_get_total_avg_sales_by_product(self, mock_get_sale_service):
        mock_service = mock_get_sale_service.return_value
        mock_service.get_total_avg_sales_by_product.return_value = [
            ProductSalesOutput(KeyProduct="1|44733", total_sales=1000.0, avg_sales=100.0)
        ]

        response = client.get("/api/v1/sales/product/total_avg")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 3)

    @patch("app.api.endpoints.sales.get_sale_service")
    def test_get_total_avg_sales_by_employee(self, mock_get_sale_service):
        mock_service = mock_get_sale_service.return_value
        mock_service.get_total_avg_sales_by_employee.return_value = [
            EmployeeSalesOutput(KeyEmployee="1|343", total_sales=1000.0, avg_sales=100.0)
        ]

        response = client.get("/api/v1/sales/employee/total_avg")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 3)


if __name__ == '__main__':
    unittest.main()
