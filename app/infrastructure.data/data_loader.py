import sys
import os
import pandas as pd


class DataLoader:
    @staticmethod
    def load_parquet_files(directory: str) -> pd.DataFrame:
        """
               Carga todos los archivos Parquet desde el directorio especificado y los combina en un único DataFrame.
               Args:
                   directory (str): La ruta del directorio que contiene los archivos Parquet.
               Returns:
                   pd.DataFrame: Un DataFrame combinado de todos los archivos Parquet.
               Raises:
                   FileNotFoundError: Si el directorio no existe o no contiene archivos Parquet.
               """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"El directorio {directory} no existe")

        files = [f for f in os.listdir(directory) if f.endswith('.parquet')]
        if not files:
            raise FileNotFoundError(f"No se encontraron archivos Parquet en el directorio {directory}")

        dataframes = [pd.read_parquet(os.path.join(directory, f)) for f in files]
        combined_df = pd.concat(dataframes, ignore_index=True)
        return combined_df
