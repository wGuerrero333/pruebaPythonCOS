import logging
from modules.excel_handler import leer_ordenes, guardar_reporte
from modules.api_client import obtener_estado_api
from modules.web_scraper import obtener_datos_libro
from config import INPUT_FILE, OUTPUT_FILE, LOG_FILE

# Configurar logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    logging.info("Inicio del proceso")

    df = leer_ordenes(INPUT_FILE)
    resultados = []

    for _, row in df.iterrows():
        orden_id = int(row["orden_id"])

        logging.info(f"Procesando orden {orden_id}")

        estado_api = obtener_estado_api(orden_id)
        titulo, precio, disponibilidad = obtener_datos_libro(orden_id)

        resultados.append({
            "orden_id": orden_id,
            "estado_api": estado_api,
            "titulo_libro": titulo,
            "precio": precio,
            "disponibilidad": disponibilidad
        })

    guardar_reporte(resultados, OUTPUT_FILE)

    logging.info("Proceso finalizado correctamente")


if __name__ == "__main__":
    main()