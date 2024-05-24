from fastapi import APIRouter, Depends, Request
from typing import List

from app.api.dependencies import oauth2_scheme
from app.domain.contracts.services.i_sale_service import ISaleService
from app.domain.inputs.product_input import ProductInput
from app.domain.inputs.store_input import StoreInput
from app.domain.inputs.employee_input import EmployeeInput
from app.domain.outputs.employee_sales_output import EmployeeSalesOutput
from app.domain.outputs.product_sales_output import ProductSalesOutput
from app.domain.outputs.sale_output import SaleOutput
from app.domain.outputs.store_sales_output import StoreSalesOutput
from app.services.sale_service import SaleService

router = APIRouter()


def get_sale_service(request: Request) -> SaleService:
    return request.state.sale_service


# Endpoint para consultar las ventas por empleado en un periodo
@router.post("/sales/employee", response_model=List[SaleOutput])
def get_sales_by_employee(input: EmployeeInput, sale_service: SaleService = Depends(get_sale_service)):
    return sale_service.get_sales_by_employee(input.KeyEmployee, input.StartDate.date(), input.EndDate.date())


# Endpoint para consultar las ventas por producto en un periodo
@router.post("/sales/product", response_model=List[SaleOutput])
def get_sales_by_product(input: ProductInput, sale_service: SaleService = Depends(get_sale_service)):
    return sale_service.get_sales_by_product(input.KeyProduct, input.StartDate.date(), input.EndDate.date())


# Endpoint para consultar las ventas por tienda en un periodo
@router.post("/sales/store", response_model=List[SaleOutput])
def get_sales_by_store(input: StoreInput, sale_service: ISaleService = Depends(get_sale_service)):
    return sale_service.get_sales_by_store(input.KeyStore, input.StartDate.date(), input.EndDate.date())


# Endpoint para consultar la venta total y promedio por tienda
@router.get("/sales/store/total_avg", response_model=List[StoreSalesOutput])
def get_total_avg_sales_by_store(sale_service: ISaleService = Depends(get_sale_service)):
    return sale_service.get_total_avg_sales_by_store()


# Endpoint para consultar la venta total y promedio por producto
@router.get("/sales/product/total_avg", response_model=List[ProductSalesOutput])
def get_total_avg_sales_by_product(sale_service: ISaleService = Depends(get_sale_service)):
    return sale_service.get_total_avg_sales_by_product()


# Endpoint para consultar la venta total y promedio por empleado
@router.get("/sales/employee/total_avg", response_model=List[EmployeeSalesOutput])
def get_total_avg_sales_by_employee(sale_service: ISaleService = Depends(get_sale_service)):
    return sale_service.get_total_avg_sales_by_employee()
