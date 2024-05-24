import os
import pandas as pd
from cachetools import TTLCache
from threading import Thread, Lock, Event
from tqdm import tqdm
import requests
from zipfile import ZipFile
from app.domain.contracts.infrastructures.i_data_loader import IDataLoader
from app.core.config import settings
from app.infrastructure.cached_property import cached_property


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
        if not os.path.exists(directory):
            self._download_and_extract_zip(directory)

        files = [f for f in os.listdir(directory) if f.endswith('.parquet')]
        if not files:
            raise FileNotFoundError(f"No se encontraron archivos Parquet en el directorio {directory}")

        self._load_complete.clear()
        if self._load_thread is None or not self._load_thread.is_alive():
            self._load_thread = Thread(target=self._load_files_in_background, args=(files, directory))
            self._load_thread.start()

        self._load_complete.wait()  # Esperar a que se complete la carga
        return self._dataframe

    def _download_and_extract_zip(self, directory: str):
        os.makedirs(directory)
        response = requests.get(settings.URL_DATA_EXAMPLE, stream=True)
        zip_path = f"{directory}.zip"
        total_size = int(response.headers.get('content-length', 0))

        with open(zip_path, 'wb') as file, tqdm(
                desc="Descargando archivo",
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                bar.update(len(data))

        with ZipFile(zip_path, 'r') as zip_ref:
            zip_info_list = zip_ref.infolist()
            for member in tqdm(zip_info_list, desc="Descomprimiendo archivo"):
                zip_ref.extract(member, directory)

    def _load_files_in_background(self, files, directory):
        for file in tqdm(files, desc="Cargando archivos"):
            df = pd.read_parquet(os.path.join(directory, file))
            with self._lock:
                self._dataframe = pd.concat([self._dataframe, df], ignore_index=True)
        self._load_complete.set()  # Indicar que la carga se ha completado

    def get_current_dataframe(self) -> pd.DataFrame:
        with self._lock:
            return self._dataframe.copy()
