from fastapi import APIRouter, Depends, Query
from typing import List

from app.api.dependencies import get_sale_service_request
from app.domain.contracts.services.i_sale_service import ISaleService
from app.domain.inputs.product_input import ProductInput
from app.domain.inputs.store_input import StoreInput
from app.domain.inputs.employee_input import EmployeeInput
from app.domain.outputs.employee_sales_output import EmployeeSalesOutput
from app.domain.outputs.product_sales_output import ProductSalesOutput
from app.domain.outputs.sale_output import SaleOutput
from app.domain.outputs.store_sales_output import StoreSalesOutput

router = APIRouter()


@router.post("/sales/employee", response_model=List[SaleOutput])
def get_sales_by_employee(
        employee: EmployeeInput,
        page: int = Query(1, ge=1, description="Número de la página. Valor por defecto: 1"),
        page_size: int = Query(10, ge=1, le=100, description="Tamaño de la página. Valor por defecto: 10"),
        sale_service: ISaleService = Depends(get_sale_service_request)
):
    """
    Endpoint para consultar las ventas por empleado en un periodo con paginación.

    :param employee: Información del empleado y las fechas de inicio y fin.
    :param page: Número de la página. Valor por defecto: 1.
    :param page_size: Tamaño de la página. Valor por defecto: 10.
    :param sale_service: Servicio de ventas inyectado por dependencia.
    :return: Lista de ventas del empleado en el periodo especificado.
    """
    return sale_service.get_sales_by_employee(employee.KeyEmployee, employee.StartDate.date(), employee.EndDate.date(),
                                              page, page_size)


@router.post("/sales/product", response_model=List[SaleOutput])
def get_sales_by_product(
        product: ProductInput,
        page: int = Query(1, ge=1, description="Número de la página. Valor por defecto: 1"),
        page_size: int = Query(10, ge=1, le=100, description="Tamaño de la página. Valor por defecto: 10"),
        sale_service: ISaleService = Depends(get_sale_service_request)
):
    """
    Endpoint para consultar las ventas por producto en un periodo con paginación.

    :param product: Información del producto y las fechas de inicio y fin.
    :param page: Número de la página. Valor por defecto: 1.
    :param page_size: Tamaño de la página. Valor por defecto: 10.
    :param sale_service: Servicio de ventas inyectado por dependencia.
    :return: Lista de ventas del producto en el periodo especificado.
    """
    return sale_service.get_sales_by_product(product.KeyProduct, product.StartDate.date(), product.EndDate.date(), page,
                                             page_size)


@router.post("/sales/store", response_model=List[SaleOutput])
def get_sales_by_store(
        store: StoreInput,
        page: int = Query(1, ge=1, description="Número de la página. Valor por defecto: 1"),
        page_size: int = Query(10, ge=1, le=100, description="Tamaño de la página. Valor por defecto: 10"),
        sale_service: ISaleService = Depends(get_sale_service_request)
):
    """
    Endpoint para consultar las ventas por tienda en un periodo con paginación.

    :param store: Información de la tienda y las fechas de inicio y fin.
    :param page: Número de la página. Valor por defecto: 1.
    :param page_size: Tamaño de la página. Valor por defecto: 10.
    :param sale_service: Servicio de ventas inyectado por dependencia.
    :return: Lista de ventas de la tienda en el periodo especificado.
    """
    return sale_service.get_sales_by_store(store.KeyStore, store.StartDate.date(), store.EndDate.date(), page,
                                           page_size)


@router.get("/sales/store/total_avg", response_model=List[StoreSalesOutput])
def get_total_avg_sales_by_store(
        page: int = Query(1, ge=1, description="Número de la página. Valor por defecto: 1"),
        page_size: int = Query(10, ge=1, le=100, description="Tamaño de la página. Valor por defecto: 10"),
        sale_service: ISaleService = Depends(get_sale_service_request)
):
    """
    Endpoint para consultar la venta total y promedio por tienda con paginación.

    :param page: Número de la página. Valor por defecto: 1.
    :param page_size: Tamaño de la página. Valor por defecto: 10.
    :param sale_service: Servicio de ventas inyectado por dependencia.
    :return: Lista de ventas totales y promedio por tienda.
    """
    return sale_service.get_total_avg_sales_by_store(page, page_size)


@router.get("/sales/product/total_avg", response_model=List[ProductSalesOutput])
def get_total_avg_sales_by_product(
        page: int = Query(1, ge=1, description="Número de la página. Valor por defecto: 1"),
        page_size: int = Query(10, ge=1, le=100, description="Tamaño de la página. Valor por defecto: 10"),
        sale_service: ISaleService = Depends(get_sale_service_request)
):
    """
    Endpoint para consultar la venta total y promedio por producto con paginación.

    :param page: Número de la página. Valor por defecto: 1.
    :param page_size: Tamaño de la página. Valor por defecto: 10.
    :param sale_service: Servicio de ventas inyectado por dependencia.
    :return: Lista de ventas totales y promedio por producto.
    """
    return sale_service.get_total_avg_sales_by_product(page, page_size)


@router.get("/sales/employee/total_avg", response_model=List[EmployeeSalesOutput])
def get_total_avg_sales_by_employee(
        page: int = Query(1, ge=1, description="Número de la página. Valor por defecto: 1"),
        page_size: int = Query(10, ge=1, le=100, description="Tamaño de la página. Valor por defecto: 10"),
        sale_service: ISaleService = Depends(get_sale_service_request)
):
    """
    Endpoint para consultar la venta total y promedio por empleado con paginación.

    :param page: Número de la página. Valor por defecto: 1.
    :param page_size: Tamaño de la página. Valor por defecto: 10.
    :param sale_service: Servicio de ventas inyectado por dependencia.
    :return: Lista de ventas totales y promedio por empleado.
    """
    return sale_service.get_total_avg_sales_by_employee(page, page_size)
