from fastapi import APIRouter, Depends
from typing import List, Dict
from datetime import datetime
from app.domain.entities.sales.sale import Sale
from app.services.sale_service import SaleService
from app.api.dependencies import create_sale_service

router = APIRouter()
