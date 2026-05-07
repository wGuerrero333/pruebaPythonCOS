"""
AGENTE RPA - Procesador Inteligente de Órdenes
Versión mejorada con validación, estadísticas y recuperación ante errores
"""

import logging
import sys
from datetime import datetime
from typing import List, Dict, Any
from modules.excel_handler import leer_ordenes, guardar_reporte
from modules.api_client import obtener_estado_api
from modules.web_scraper import obtener_datos_libro
from config import INPUT_FILE, OUTPUT_FILE, LOG_FILE


class AgenteRPA:
    """Agente inteligente para procesar órdenes de compra"""
    
    def __init__(self):
        """Inicializa el agente con logging configurado"""
        self.logger = self._configurar_logging()
        self.resultados: List[Dict[str, Any]] = []
        self.estadisticas = {
            "total_ordenes": 0,
            "ordenes_exitosas": 0,
            "ordenes_con_error": 0,
            "estados": {"Aprobada": 0, "En revisión": 0, "Error_A": 0},
            "tiempo_inicio": None,
            "tiempo_fin": None
        }
    
    def _configurar_logging(self) -> logging.Logger:
        """Configura el sistema de logging"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        # Handler para archivo
        handler_archivo = logging.FileHandler(LOG_FILE)
        handler_archivo.setLevel(logging.INFO)
        
        # Handler para consola
        handler_consola = logging.StreamHandler(sys.stdout)
        handler_consola.setLevel(logging.INFO)
        
        # Formato de logs
        formato = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler_archivo.setFormatter(formato)
        handler_consola.setFormatter(formato)
        
        logger.addHandler(handler_archivo)
        logger.addHandler(handler_consola)
        
        return logger
    
    def cargar_ordenes(self) -> bool:
        """
        Carga las órdenes desde el archivo Excel
        
        Returns:
            bool: True si carga exitosamente, False en caso contrario
        """
        try:
            self.logger.info("Cargando órdenes desde: " + INPUT_FILE)
            self.df = leer_ordenes(INPUT_FILE)
            self.estadisticas["total_ordenes"] = len(self.df)
            self.logger.info(f"✓ Se cargaron {self.estadisticas['total_ordenes']} órdenes")
            return True
        except FileNotFoundError:
            self.logger.error(f"✗ Archivo no encontrado: {INPUT_FILE}")
            return False
        except Exception as e:
            self.logger.error(f"✗ Error al cargar órdenes: {str(e)}")
            return False
    
    def procesar_orden(self, orden_id: int, indice: int) -> Dict[str, Any]:
        """
        Procesa una orden individual
        
        Args:
            orden_id: ID de la orden a procesar
            indice: Índice actual del procesamiento (para progressbar)
        
        Returns:
            Dict con los resultados de la orden
        """
        try:
            self.logger.info(
                f"[{indice}/{self.estadisticas['total_ordenes']}] "
                f"Procesando orden: {orden_id}"
            )
            
            # Obtener estado de la API
            estado_api = obtener_estado_api(orden_id)
            
            # Obtener datos del libro
            titulo, precio, disponibilidad = obtener_datos_libro(orden_id)
            
            resultado = {
                "orden_id": orden_id,
                "estado_api": estado_api,
                "titulo_libro": titulo or "N/A",
                "precio": precio or "N/A",
                "disponibilidad": disponibilidad or "N/A"
            }
            
            # Actualizar estadísticas
            self.estadisticas["estados"][estado_api] = \
                self.estadisticas["estados"].get(estado_api, 0) + 1
            
            if estado_api != "Error_A" and titulo:
                self.estadisticas["ordenes_exitosas"] += 1
                self.logger.debug(f"✓ Orden {orden_id} procesada exitosamente")
            else:
                self.estadisticas["ordenes_con_error"] += 1
                self.logger.warning(
                    f"⚠ Orden {orden_id}: Estado={estado_api}, Título={'Obtenido' if titulo else 'No disponible'}"
                )
            
            return resultado
            
        except Exception as e:
            self.logger.error(f"✗ Error procesando orden {orden_id}: {str(e)}")
            self.estadisticas["ordenes_con_error"] += 1
            return {
                "orden_id": orden_id,
                "estado_api": "Error_A",
                "titulo_libro": "ERROR",
                "precio": "ERROR",
                "disponibilidad": "ERROR"
            }
    
    def procesar_todas_ordenes(self) -> bool:
        """
        Procesa todas las órdenes cargadas
        
        Returns:
            bool: True si el procesamiento fue exitoso
        """
        if self.df is None:
            self.logger.error("No hay órdenes cargadas")
            return False
        
        self.resultados = []
        
        try:
            for indice, (_, row) in enumerate(self.df.iterrows(), 1):
                orden_id = int(row["orden_id"])
                resultado = self.procesar_orden(orden_id, indice)
                self.resultados.append(resultado)
            
            self.logger.info(f"✓ Procesamiento completado: {len(self.resultados)} órdenes")
            return True
            
        except Exception as e:
            self.logger.error(f"✗ Error durante el procesamiento: {str(e)}")
            return False
    
    def guardar_resultados(self) -> bool:
        """
        Guarda los resultados en un archivo Excel
        
        Returns:
            bool: True si se guardó correctamente
        """
        try:
            self.logger.info(f"Guardando reporte en: {OUTPUT_FILE}")
            guardar_reporte(self.resultados, OUTPUT_FILE)
            self.logger.info(f"✓ Reporte guardado exitosamente")
            return True
        except Exception as e:
            self.logger.error(f"✗ Error al guardar reporte: {str(e)}")
            return False
    
    def generar_resumen(self) -> str:
        """
        Genera un resumen estadístico del procesamiento
        
        Returns:
            str: Resumen formateado
        """
        tasa_exito = (self.estadisticas["ordenes_exitosas"] / 
                     self.estadisticas["total_ordenes"] * 100) \
                     if self.estadisticas["total_ordenes"] > 0 else 0
        
        resumen = f"""
╔════════════════════════════════════════════════════════════╗
║           RESUMEN DEL PROCESAMIENTO RPA                    ║
╠════════════════════════════════════════════════════════════╣
║ Total de órdenes procesadas:    {self.estadisticas['total_ordenes']:>15}        ║
║ Órdenes exitosas:               {self.estadisticas['ordenes_exitosas']:>15}        ║
║ Órdenes con error:              {self.estadisticas['ordenes_con_error']:>15}        ║
║ Tasa de éxito:                  {tasa_exito:>14.1f}%       ║
╠════════════════════════════════════════════════════════════╣
║ ESTADOS DE API:                                            ║
║   - Aprobadas:                  {self.estadisticas['estados']['Aprobada']:>15}        ║
║   - En revisión:                {self.estadisticas['estados']['En revisión']:>15}        ║
║   - Errores:                    {self.estadisticas['estados']['Error_A']:>15}        ║
╠════════════════════════════════════════════════════════════╣
║ Archivo de salida:  {OUTPUT_FILE:<45} ║
╚════════════════════════════════════════════════════════════╝
"""
        return resumen
    
    def ejecutar(self) -> bool:
        """
        Ejecuta el flujo completo del agente RPA
        
        Returns:
            bool: True si la ejecución fue exitosa
        """
        self.estadisticas["tiempo_inicio"] = datetime.now()
        
        self.logger.info("=" * 60)
        self.logger.info("INICIANDO AGENTE RPA DE PROCESAMIENTO DE ÓRDENES")
        self.logger.info("=" * 60)
        
        # Paso 1: Cargar órdenes
        if not self.cargar_ordenes():
            self.logger.error("No se pudieron cargar las órdenes")
            return False
        
        # Paso 2: Procesar todas las órdenes
        if not self.procesar_todas_ordenes():
            self.logger.error("Error durante el procesamiento de órdenes")
            return False
        
        # Paso 3: Guardar resultados
        if not self.guardar_resultados():
            self.logger.error("No se pudieron guardar los resultados")
            return False
        
        # Paso 4: Generar resumen
        self.estadisticas["tiempo_fin"] = datetime.now()
        tiempo_total = (self.estadisticas["tiempo_fin"] - 
                       self.estadisticas["tiempo_inicio"]).total_seconds()
        
        self.logger.info(self.generar_resumen())
        self.logger.info(f"Tiempo total de ejecución: {tiempo_total:.2f} segundos")
        self.logger.info("=" * 60)
        self.logger.info("PROCESO FINALIZADO CORRECTAMENTE ✓")
        self.logger.info("=" * 60)
        
        return True


def main():
    """Punto de entrada del agente RPA"""
    agente = AgenteRPA()
    exito = agente.ejecutar()
    sys.exit(0 if exito else 1)


if __name__ == "__main__":
    main()
