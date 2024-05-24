import sys
import unittest
import os
import pandas as pd
from cachetools import TTLCache
from pandas.testing import assert_frame_equal
from app.domain.contracts.infrastructures.i_data_loader import IDataLoader
from app.infrastructure.data.data_loader import DataLoader

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

class TestDataLoader(unittest.TestCase):
    data_loader: IDataLoader = None

    def setUp(self):
        # Crear un directorio de prueba
        self.test_dir = 'test_data'
        os.makedirs(self.test_dir, exist_ok=True)

        # Crear algunos archivos Parquet de prueba
        self.df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        self.df2 = pd.DataFrame({'A': [7, 8, 9], 'B': [10, 11, 12]})

        self.df1.to_parquet(os.path.join(self.test_dir, 'test1.parquet'))
        self.df2.to_parquet(os.path.join(self.test_dir, 'test2.parquet'))
        cache = TTLCache(maxsize=1, ttl=360)
        self.data_loader = DataLoader(cache)

    def tearDown(self):
        # Asegurarse de que el hilo de carga en segundo plano se haya completado
        if self.data_loader._load_thread:
            self.data_loader._load_thread.join()
        # Eliminar los archivos y el directorio de prueba después de cada prueba
        for f in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, f))
        os.rmdir(self.test_dir)

    def test_load_parquet_files_success(self):
        # Probar la carga exitosa de archivos Parquet

        combined_df = self.data_loader.load_parquet_files(self.test_dir)
        expected_df = pd.concat([self.df1, self.df2], ignore_index=True)
        assert_frame_equal(combined_df, expected_df)

    def test_load_parquet_files_no_directory(self):
        # Probar que se lanza una excepción si el directorio no existe
        with self.assertRaises(FileNotFoundError):
            self.data_loader.load_parquet_files('non_existent_directory')

    def test_load_parquet_files_empty_directory(self):
        # Probar que se lanza una excepción si el directorio no contiene archivos Parquet
        empty_dir = 'empty_dir'
        os.makedirs(empty_dir, exist_ok=True)
        try:
            with self.assertRaises(FileNotFoundError):
                self.data_loader.load_parquet_files(empty_dir)
        finally:
            os.rmdir(empty_dir)

if __name__ == '__main__':
    unittest.main()