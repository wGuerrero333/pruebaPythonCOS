import requests
import time
from config import API_URL, TIMEOUT
# se importa las variables de config.py para usar la URL de la API y el tiempo de espera en las solicitudes
def obtener_estado_api(orden_id, reintentos=3):
    url = f"{API_URL}{orden_id}"

    for intento in range(reintentos):
        try:
            response = requests.get(url, timeout=TIMEOUT)
# si el status es 200-299 es decir hubo exito devuleve Aprobada o En revisión

            if 200 <= response.status_code < 300:
                data = response.json()
                return "Aprobada" if data.get("completed") else "En revisión"
# si el status es 500 es decir hubo error devuleve ERROR A
            elif 400 <= response.status_code < 500:
                return "Error_A"

            elif 500 <= response.status_code < 600:
                time.sleep(2)  # espera 2 segundos antes de reintentar

        except requests.exceptions.Timeout:
            time.sleep(2)

    return "Error_A"