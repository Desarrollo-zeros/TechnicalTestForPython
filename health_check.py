import os
import requests
import sys
from dotenv import load_dotenv
import time

def health_check(url, intentos=3):

    for intento in range(intentos):
        try:
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                print(f"¡Verificación de servidor activo Link {url}!")
                return True
            else:
                print(f"Fallo en la verificación de salud con el código de estado: {respuesta.status_code}")
        except Exception as e:
            print(f"Fallo en la verificación de salud con excepción: {e}")

        if intento < intentos - 1:
            print(f"Reintentando... ({intento + 1}/{intentos})")
            time.sleep(30)  # Esperar 5 segundos antes de reintentar

    print("Fallo en la verificación de salud después de varios intentos")
    return False

if __name__ == "__main__":
    load_dotenv()
    url = os.getenv("URL_HEALTH") + "/health"
    if not health_check(url):
        sys.exit(1)
