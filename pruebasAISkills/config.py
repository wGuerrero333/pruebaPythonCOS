import os
from dotenv import load_dotenv
# Busca un archivo llamado .env en el directorio actual y carga las variables de entorno definidas en él.   
load_dotenv()

# Busca la variable "API_URL" en el entorno del sistema operativo.
# Si existe → la usa
# Si NO existe → usa el valor por defecto max espera 5 segundos para la respuesta de la API
API_URL = os.getenv("API_URL", "https://jsonplaceholder.typicode.com/todos/")
TIMEOUT = 5 

# Ruta del archivo de entrada

# ✔ Busca en .env
# ✔ Si no existe → usa "data/ordenes.xlsx"

INPUT_FILE = os.getenv("INPUT_FILE", "data/ordenes.xlsx")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "data/reporte_final.xlsx")

# Configuración de MySQL
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "administradorNuevo")
DB_PASSWORD = os.getenv("DB_PASSWORD", "#Delcamino333")
DB_NAME = os.getenv("DB_NAME", "scraptLibros")

# Define la ruta del archivo de logs
# ✔ No usa .env (valor fijo)
# ✔ Guarda mensajes del sistema (errores, ejecución, etc.)
LOG_FILE = "logs/proceso.log"