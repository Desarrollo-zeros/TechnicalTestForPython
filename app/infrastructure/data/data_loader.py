import os
import pandas as pd
from cachetools import TTLCache
from threading import Thread, Lock, Event
from app.domain.contracts.infrastructures.i_data_loader import IDataLoader
from app.core.config import settings

"""Se creo un decorador custom para poder obtener configurar la data en cache"""


def cached_property(func):
    """Decorator to cache instance property values."""

    def wrapper(self, *args, **kwargs):
        if not hasattr(self, '_cache'):
            self._cache = TTLCache(maxsize=settings.MAX_SIZE_CACHE, ttl=settings.TTL_CACHE)
        key = (func.__name__, args, frozenset(kwargs.items()))
        if key not in self._cache:
            self._cache[key] = func(self, *args, **kwargs)
        return self._cache[key]

    return wrapper


class DataLoader(IDataLoader):
    def __init__(self, cache: TTLCache):
        super().__init__()
        self._cache = cache
        self._dataframe = pd.DataFrame()
        self._load_thread = None
        self._lock = Lock()
        self._load_complete = Event()

    @cached_property
    def load_parquet_files(self, directory: str) -> pd.DataFrame:
        """
        Carga todos los archivos Parquet desde el directorio especificado y los combina en un único DataFrame.
        Esta operación se realiza en segundo plano.

        Args:
            directory (str): La ruta del directorio que contiene los archivos Parquet.

        Returns:
            pd.DataFrame: Un DataFrame combinado de todos los archivos Parquet.

        Raises:
            FileNotFoundError: Si el directorio no existe o no contiene archivos Parquet.
            :param directory:
            :return:
        """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"El directorio {directory} no existe")

        files = [f for f in os.listdir(directory) if f.endswith('.parquet')]
        if not files:
            raise FileNotFoundError(f"No se encontraron archivos Parquet en el directorio {directory}")

        self._load_complete.clear()
        if self._load_thread is None or not self._load_thread.is_alive():
            self._load_thread = Thread(target=self._load_files_in_background, args=(files, directory))
            self._load_thread.start()

        self._load_complete.wait()  # Esperar a que se complete la carga
        return self._dataframe

    def _load_files_in_background(self, files, directory):
        for file in files:
            df = pd.read_parquet(os.path.join(directory, file))
            with self._lock:
                self._dataframe = pd.concat([self._dataframe, df], ignore_index=True)
        self._load_complete.set()  # Indicar que la carga se ha completado

    def get_current_dataframe(self) -> pd.DataFrame:
        with self._lock:
            return self._dataframe.copy()
