import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "https://jsonplaceholder.typicode.com/todos/")
TIMEOUT = 5

INPUT_FILE = os.getenv("INPUT_FILE", "data/ordenes.xlsx")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "data/reporte_final.xlsx")

LOG_FILE = "logs/proceso.log"