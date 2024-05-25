from cachetools import TTLCache
from fastapi.security import OAuth2PasswordBearer
from fastapi import Request
from app.domain.contracts.infrastructures.i_data_frame_manager import IDataFrameManager
from app.domain.contracts.infrastructures.i_data_loader import IDataLoader
from app.domain.contracts.services.I_user_service import IUserService
from app.domain.contracts.services.i_sale_service import ISaleService
from app.infrastructure.data.data_loader import DataLoader
from app.infrastructure.data.data_frame_manager import DataFrameManager
from app.services.user_service import UserService
from app.services.sale_service import SaleService
from app.core.config import settings
from threading import Lock


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()  # Para asegurar la thread-safety

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class SaleServiceSingleton(metaclass=SingletonMeta):
    def __init__(self):
        _cache = TTLCache(maxsize=settings.MAX_SIZE_CACHE, ttl=settings.TTL_CACHE)
        data_loader: IDataLoader = DataLoader(_cache)
        data_manager: IDataFrameManager = DataFrameManager(data_loader, settings.DATA_DIRECTORY)
        self._sale_service: ISaleService = SaleService(data_manager)

    def get_service(self) -> ISaleService:
        return self._sale_service


# Uso del singleton para obtener la instancia de SaleService
def get_sale_service() -> ISaleService:
    singleton_instance = SaleServiceSingleton()
    return singleton_instance.get_service()


def get_user_service() -> IUserService:
    user_service: IUserService = UserService()
    return user_service


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")


def get_sale_service_request(request: Request) -> SaleService:
    return request.state.sale_service


def get_user_service_request(request: Request) -> UserService:
    return request.state.user_service
