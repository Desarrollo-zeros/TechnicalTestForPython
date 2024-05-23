from cachetools import TTLCache
from app.domain.contracts.infrastructures.i_data_frame_manager import IDataFrameManager
from app.domain.contracts.infrastructures.i_data_loader import IDataLoader
from app.domain.contracts.services.i_sale_service import ISaleService
from app.infrastructure.data.data_loader import DataLoader
from app.infrastructure.data.data_frame_manager import DataFrameManager
from app.services.sale_service import SaleService
from app.core.config import settings


def create_sale_service() -> ISaleService:
    _cache = TTLCache(maxsize=settings.MAX_SIZE_CACHE, ttl=settings.TTL_CACHE)
    data_loader: IDataLoader = DataLoader(_cache)
    data_manager: IDataFrameManager = DataFrameManager(data_loader, settings.DATA_DIRECTORY)
    sale_service: ISaleService = SaleService(data_manager)
    return sale_service
