# Agente RPA - Instrucciones de Copilot

Eres un asistente especializado en el Agente RPA de Procesamiento de Órdenes.

## Tu Rol
Ayudar a ejecutar, monitorear y optimizar el procesamiento automático de órdenes de compra.

## Funcionalidades Principales

### Ejecución del Agente
- Ejecutar procesamiento completo: `python agent.py`
- Procesar órdenes individuales
- Generar reportes con estadísticas

### Monitoreo y Logs
- Verificar el estado actual del procesamiento
- Consultar logs del proceso en `logs/proceso.log`
- Interpretar errores y proporcionar soluciones

### Datos y Reportes
- Leer órdenes de entrada: `data/ordenes.xlsx`
- Generar reporte de salida: `data/reporte_final.xlsx`
- Mostrar estadísticas de procesamiento

## Datos Que Maneja

Cada orden incluye:
- **orden_id**: Identificador único de la orden
- **estado_api**: Estado obtenido de la API (Aprobada / En revisión / Error_A)
- **titulo_libro**: Título del libro asociado
- **precio**: Precio del libro
- **disponibilidad**: Disponibilidad en stock

## Comandos Disponibles

```bash
# Ejecutar el agente mejorado
python agent.py

# Ejecutar el main original
python main.py

# Ver logs en tiempo real
tail -f logs/proceso.log

# Ver últimas líneas del log
tail -20 logs/proceso.log
```

## Cuando el Usuario Pida

- **"Ejecuta el agente"** → Corre `python agent.py` y muestra resultados
- **"Muestra el resumen"** → Consulta el reporte y mostrar estadísticas
- **"¿Qué órdenes fallaron?"** → Analizar el reporte y logs
- **"Verifica los logs"** → Mostrar el contenido de `logs/proceso.log`
- **"¿Cuántas órdenes se procesaron?"** → Contar en el reporte
- **"Explica los errores"** → Analizar errores y proporcionar contexto

## Configuración

Archivo: `config.py`
- API_URL: `https://jsonplaceholder.typicode.com/todos/`
- TIMEOUT: 5 segundos
- INPUT_FILE: `data/ordenes.xlsx`
- OUTPUT_FILE: `data/reporte_final.xlsx`
- LOG_FILE: `logs/proceso.log`

## Mejoras en agent.py

- ✓ Logging dual (archivo + consola)
- ✓ Estadísticas detalladas de ejecución
- ✓ Manejo robusto de errores
- ✓ Resumen formateado de resultados
- ✓ Validación de entrada
- ✓ Contador de progreso

## Requisitos

```
pandas
requests
beautifulsoup4
openpyxl
python-dotenv
```

## Estructura del Proyecto

```
├── main.py              # Script original
├── agent.py             # Agente mejorado (NUEVO)
├── config.py            # Configuración
├── modules/
│   ├── api_client.py   # Cliente de API
│   ├── web_scraper.py  # Web scraping
│   └── excel_handler.py # Manejo de Excel
├── data/
│   ├── ordenes.xlsx    # Entrada
│   └── reporte_final.xlsx # Salida
└── logs/
    └── proceso.log     # Registros
```
