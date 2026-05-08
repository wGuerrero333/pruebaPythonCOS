import logging
from typing import List, Dict, Any
import mysql.connector
from mysql.connector import Error
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


def obtener_conexion_sin_db():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD
    )


def obtener_conexion():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def crear_base_datos():
    try:
        conn = obtener_conexion_sin_db()
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.commit()
        logging.info(f"✔ Base de datos '{DB_NAME}' verificada/creada")
        cursor.close()
        conn.close()
        return True
    except Error as e:
        logging.error(f"✗ Error al crear base de datos: {e}")
        return False


def crear_tabla():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reporte_ordenes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                orden_id INT NOT NULL,
                estado_api VARCHAR(50),
                titulo_libro VARCHAR(255),
                precio VARCHAR(50),
                disponibilidad VARCHAR(100),
                fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        logging.info("✔ Tabla 'reporte_ordenes' verificada/creada")
        cursor.close()
        conn.close()
        return True
    except Error as e:
        logging.error(f"✗ Error al crear tabla: {e}")
        return False


def guardar_en_mysql(data: List[Dict[str, Any]]):
    if not data:
        logging.warning("No hay datos para guardar en MySQL")
        return False

    try:
        conn = obtener_conexion()
        cursor = conn.cursor()

        sql = """
            INSERT INTO reporte_ordenes 
            (orden_id, estado_api, titulo_libro, precio, disponibilidad)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = [
            (
                d["orden_id"],
                d.get("estado_api", "N/A"),
                d.get("titulo_libro", "N/A"),
                d.get("precio", "N/A"),
                d.get("disponibilidad", "N/A")
            )
            for d in data
        ]

        cursor.executemany(sql, valores)
        conn.commit()
        logging.info(f"✔ {len(valores)} registros guardados en MySQL (tabla: reporte_ordenes)")
        cursor.close()
        conn.close()
        return True

    except Error as e:
        logging.error(f"✗ Error al guardar en MySQL: {e}")
        return False


def leer_desde_mysql() -> List[Dict[str, Any]]:
    try:
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reporte_ordenes ORDER BY orden_id")
        registros = cursor.fetchall()
        cursor.close()
        conn.close()
        logging.info(f"✔ {len(registros)} registros leídos desde MySQL")
        return registros
    except Error as e:
        logging.error(f"✗ Error al leer desde MySQL: {e}")
        return []
