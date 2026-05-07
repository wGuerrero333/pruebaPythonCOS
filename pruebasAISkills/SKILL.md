---
description: Agente RPA especializado en procesamiento automático de órdenes de compra con validación de API y web scraping
tags: [rpa, automation, excel, api, webscraping, ordenes, reporte]
---

# SKILL: Agente RPA - Procesador de Órdenes

## 📋 Descripción General

Agente inteligente especializado en procesar órdenes de compra de forma automatizada. Integra consultas a API, web scraping, y generación de reportes en un flujo RPA completo con logging, validación de datos y manejo robusto de errores.

**Versión**: 2.0  
**Tipo**: Automation Agent  
**Lenguaje**: Python 3.7+  
**Estado**: Production-Ready ✓

---

## 🎯 Skills Principales

### 1. **Lectura y Validación de Órdenes**
Carga y valida órdenes desde archivos Excel con manejo robusto de errores.

**Métodos Disponibles**:
- `cargar_ordenes()` - Carga órdenes del archivo Excel
- Validación automática de formato
- Manejo de excepciones (archivo no encontrado, formato incorrecto)

**Entrada**: `data/ordenes.xlsx`  
**Salida**: DataFrame con órdenes validadas  
**Errores Manejados**:
- `FileNotFoundError` - Archivo no existe
- `ValueError` - Formato Excel incorrecto
- `Exception` - Errores inesperados

**Ejemplo**:
```python
agente = AgenteRPA()
agente.cargar_ordenes()  # Carga 50+ órdenes del archivo
```

---

### 2. **Consulta de Estado en API**
Obtiene el estado de cada orden desde una API REST con reintentos automáticos.

**Métodos Disponibles**:
- `obtener_estado_api(orden_id, reintentos=3)` - Consulta estado de la orden
- Reintentos automáticos con backoff exponencial
- Manejo de timeouts y errores HTTP

**Endpoints**:
- URL: `https://jsonplaceholder.typicode.com/todos/{orden_id}`
- Método: `GET`
- Timeout: 5 segundos (configurable)

**Estados Retornados**:
- `"Aprobada"` - Tarea completada (completed=true)
- `"En revisión"` - Tarea pendiente (completed=false)
- `"Error_A"` - Error en solicitud (4xx/5xx)

**Reintentos**:
- Máximo: 3 intentos
- Espera entre intentos: 2 segundos
- Aplica solo a errores 5xx y timeouts

**Ejemplo**:
```python
estado = obtener_estado_api(1)  # "Aprobada"
estado = obtener_estado_api(999)  # "En revisión"
```

---

### 3. **Web Scraping de Libros**
Extrae datos de libros desde sitios web con parseo HTML.

**Métodos Disponibles**:
- `obtener_datos_libro(orden_id)` - Extrae título, precio, disponibilidad
- Uso de BeautifulSoup4 para parseo
- Selección por posición según orden_id

**Fuente de Datos**:
- URL: `https://books.toscrape.com/catalogue/page-1.html`
- Selector: `article.product_pod`
- Extrae: título, precio, disponibilidad

**Datos Extraídos**:
- `titulo` (string) - Nombre del libro
- `precio` (string) - Precio con símbolo (ej: £15.39)
- `disponibilidad` (string) - Estado de stock

**Manejo de Errores**:
- Retorna `None` si los datos no están disponibles
- Continúa procesamiento incluso con fallos
- Logs de errores para debugging

**Ejemplo**:
```python
titulo, precio, disponibilidad = obtener_datos_libro(1)
# Retorna: ("Sapiens: A Brief History of Humankind", "£19.99", "In stock")
```

---

### 4. **Procesamiento Iterativo de Órdenes**
Procesa cada orden de forma individual con contador de progreso.

**Métodos Disponibles**:
- `procesar_orden(orden_id, indice)` - Procesa una orden individual
- `procesar_todas_ordenes()` - Procesa todas las órdenes

**Proceso por Orden**:
1. Obtiene estado de API
2. Extrae datos del libro (web scraping)
3. Almacena resultado en estructura
4. Actualiza estadísticas
5. Registra en logs

**Contador de Progreso**:
- Formato: `[N/Total] Procesando orden...`
- Ejemplo: `[25/100] Procesando orden: 42`

**Estadísticas en Tiempo Real**:
- Total de órdenes
- Órdenes exitosas
- Órdenes con error
- Desglose por estado de API

---

### 5. **Generación de Reportes en Excel**
Crea reportes consolidados en formato Excel con resultados completos.

**Métodos Disponibles**:
- `guardar_resultados()` - Guarda reporte en Excel
- Formato: `.xlsx` (Excel moderno)
- Índices automáticos

**Estructura del Reporte**:
```
orden_id | estado_api | titulo_libro | precio | disponibilidad
---------|------------|--------------|--------|----------------
1        | Aprobada   | Book Title   | £19.99 | In stock
2        | En revisión| Book Title 2 | £14.99 | Out of Stock
```

**Ubicación de Salida**:
- Ruta: `data/reporte_final.xlsx`
- Formato: Excel 2007+ (.xlsx)
- Overwrite: Sí (reemplaza versión anterior)

**Ejemplo**:
```python
agente.guardar_resultados()  # Genera reporte_final.xlsx
```

---

### 6. **Logging Dual y Auditoría**
Sistema de logging que registra en archivo y consola simultáneamente.

**Métodos Disponibles**:
- `_configurar_logging()` - Configura sistema de logs
- Logs en archivo y stdout
- Timestamps automáticos

**Niveles de Log**:
- `INFO` - Eventos normales (carga, procesamiento)
- `WARNING` - Datos incompletos o estados no óptimos
- `ERROR` - Fallos en procesamiento
- `DEBUG` - Detalles de ejecución

**Archivo de Logs**:
- Ruta: `logs/proceso.log`
- Rotación: Manual (comando manual para limpiar)
- Formato: `YYYY-MM-DD HH:MM:SS - LEVEL - MESSAGE`

**Destinos**:
- Archivo: Persistencia permanente
- Consola: Visualización en tiempo real

**Ejemplo de Log**:
```
2026-05-04 14:30:15 - INFO - Cargando órdenes desde: data/ordenes.xlsx
2026-05-04 14:30:16 - INFO - ✓ Se cargaron 50 órdenes
2026-05-04 14:30:17 - INFO - [1/50] Procesando orden: 1
2026-05-04 14:30:18 - WARNING - ⚠ Orden 15: Estado=Error_A, Título=No disponible
```

---

### 7. **Estadísticas y Análisis**
Recopila y presenta estadísticas detalladas del procesamiento.

**Métodos Disponibles**:
- `generar_resumen()` - Genera resumen formateado
- Cálculo automático de tasas de éxito

**Estadísticas Capturadas**:
- `total_ordenes` - Cantidad total procesada
- `ordenes_exitosas` - Con estado ≠ Error_A
- `ordenes_con_error` - Fallidas o sin datos
- `estados` - Desglose: Aprobada, En revisión, Error_A
- `tiempo_inicio/fin` - Timestamps de ejecución

**Cálculos Realizados**:
- Tasa de éxito: (exitosas / total) × 100
- Tiempo total de ejecución
- Velocidad: órdenes por segundo

**Formato del Resumen**:
```
╔════════════════════════════════════════════════════════════╗
║           RESUMEN DEL PROCESAMIENTO RPA                    ║
╠════════════════════════════════════════════════════════════╣
║ Total de órdenes procesadas:                           50  ║
║ Órdenes exitosas:                                      48  ║
║ Órdenes con error:                                      2  ║
║ Tasa de éxito:                                       96.0% ║
║ ESTADOS DE API:                                            ║
║   - Aprobadas:                                         30  ║
║   - En revisión:                                       18  ║
║   - Errores:                                            2  ║
╚════════════════════════════════════════════════════════════╝
```

---

### 8. **Validación y Manejo de Errores**
Valida datos de entrada y maneja excepciones robustamente.

**Validaciones Realizadas**:
- Existencia del archivo Excel
- Formato correcto del Excel
- Columnas requeridas (orden_id)
- Valores numéricos válidos

**Manejo de Errores**:
- Try-catch para cada operación crítica
- Recuperación graceful ante fallos
- Continuación del procesamiento ante errores individuales
- Registro detallado en logs

**Estrategia**:
- Fallos de orden individual no detienen el proceso
- Fallos críticos (archivo no existe) abortan limpiamente
- Retorna `None` para datos no disponibles

**Ejemplo**:
```python
# Si falla obtener_datos_libro(), retorna (None, None, None)
# y el agente continúa con la siguiente orden
```

---

## 🔄 Flujo Completo de Ejecución

```
┌─────────────────────────────────────────────────────────┐
│ 1. INICIALIZACIÓN                                       │
│    └─ Crear instancia AgenteRPA                         │
│    └─ Configurar logging (archivo + consola)            │
│    └─ Inicializar estadísticas                          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. CARGA DE DATOS                                       │
│    └─ cargar_ordenes() → Excel a DataFrame              │
│    └─ Validar columnas y tipo de datos                  │
│    └─ Contar total de órdenes                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. PROCESAMIENTO ITERATIVO (para cada orden)            │
│    ├─ obtener_estado_api(orden_id)                      │
│    │  └─ Con reintentos (máx 3)                         │
│    │  └─ Espera 2s entre reintentos                     │
│    ├─ obtener_datos_libro(orden_id)                     │
│    │  └─ Web scraping                                   │
│    │  └─ Parseo HTML                                    │
│    ├─ Almacenar resultado                               │
│    ├─ Actualizar estadísticas                           │
│    └─ Registrar en logs                                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. GENERACIÓN DE REPORTE                                │
│    └─ guardar_reporte() → Excel                         │
│    └─ Formato: datos/reporte_final.xlsx                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 5. RESUMEN Y CIERRE                                     │
│    ├─ generar_resumen() → Tabla formateada              │
│    ├─ Mostrar estadísticas                              │
│    ├─ Registrar tiempo total                            │
│    └─ Retornar código de salida (0=éxito, 1=error)      │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Configuración

**Archivo**: `config.py`

| Parámetro | Valor Predeterminado | Descripción |
|-----------|---------------------|-------------|
| `API_URL` | `https://jsonplaceholder.typicode.com/todos/` | Endpoint de la API |
| `TIMEOUT` | `5` | Timeout de conexión (segundos) |
| `INPUT_FILE` | `data/ordenes.xlsx` | Archivo de entrada |
| `OUTPUT_FILE` | `data/reporte_final.xlsx` | Archivo de salida |
| `LOG_FILE` | `logs/proceso.log` | Archivo de logs |

**Variables de Entorno** (`.env`):
```
API_URL=https://jsonplaceholder.typicode.com/todos/
INPUT_FILE=data/ordenes.xlsx
OUTPUT_FILE=data/reporte_final.xlsx
TIMEOUT=5
```

---

## 📦 Dependencias

```
pandas==2.2.2          # Manipulación de Excel
requests==2.31.0       # Llamadas HTTP
beautifulsoup4==4.12.3 # Web scraping
openpyxl==3.1.2        # Generación de Excel
python-dotenv==1.0.1   # Manejo de .env
```

---

## 🚀 Uso

### Ejecución del Agente
```bash
# Ejecutar procesamiento completo
python agent.py

# Ejecutar en modo verbose
python agent.py 2>&1 | tee execution.log
```

### Monitoreo en Tiempo Real
```bash
# Ver logs en vivo
tail -f logs/proceso.log

# Ver últimas 20 líneas
tail -20 logs/proceso.log

# Buscar errores
grep "ERROR" logs/proceso.log
```

### Verificar Resultados
```bash
# Ver reporte generado (requiere Excel o LibreOffice)
libreoffice data/reporte_final.xlsx

# Contar órdenes procesadas
python -c "import pandas as pd; df = pd.read_excel('data/reporte_final.xlsx'); print(f'Total: {len(df)}')"
```

---

## 📊 Casos de Uso

### Uso 1: Procesamiento Rutinario
Ejecutar diariamente para procesar nuevas órdenes:
```bash
# Ejecutar cada día a las 06:00 AM (cron)
0 6 * * * /usr/bin/python3 /home/user/agent.py
```

### Uso 2: Validación de Órdenes
Verificar estado de órdenes específicas:
```python
agente = AgenteRPA()
agente.cargar_ordenes()
resultado = agente.procesar_orden(42, 1)
print(resultado["estado_api"])
```

### Uso 3: Reporte Mensual
Generar reportes consolidados:
```bash
# Procesar todas las órdenes del mes
python agent.py
# Ver: data/reporte_final.xlsx
```

---

## ✅ Validación y Testing

### Test de Carga
```bash
# Procesar 100+ órdenes
# Resultado esperado: tasa de éxito > 90%
python agent.py
```

### Test de Errores
```bash
# Verificar manejo de API no disponible
# Usar mock de API que retorna 500
# Resultado esperado: reintentos automáticos, estado "Error_A"
```

### Test de Logs
```bash
# Verificar consistencia de logs
grep -c "ERROR" logs/proceso.log
grep -c "INFO" logs/proceso.log
```

---

## 🔍 Troubleshooting

| Problema | Causa | Solución |
|----------|-------|----------|
| `FileNotFoundError` | No existe `data/ordenes.xlsx` | Crear archivo o verificar ruta |
| `ImportError: No module named 'pandas'` | Dependencias no instaladas | `pip install -r requirements.txt` |
| `Timeout Error` | API lenta o no disponible | Aumentar `TIMEOUT` en `config.py` |
| Reporte vacío | Todas las órdenes fallaron | Revisar logs para detalles de error |
| Logs no se crean | Carpeta `logs/` no existe | `mkdir -p logs` |

---

## 📝 Notas de Versión

**v2.0** (Actual)
- ✅ Logging dual (archivo + consola)
- ✅ Estadísticas detalladas
- ✅ Resumen formateado
- ✅ Validación robusta de datos
- ✅ Manejo completo de errores

**v1.0** (Original)
- Procesamiento básico
- Logging en archivo
- Sin estadísticas

---

## 🤝 Integración con VS Code Copilot

Este skill está optimizado para usarse con:
- **Copilot Chat**: Hacer preguntas sobre el estado de procesamiento
- **Copilot Inline**: Generar comandos de ejecución
- **Copilot Edits**: Modificar configuración y parámetros

**Comandos Recomendados**:
```
- "¿Cuántas órdenes se procesaron?"
- "Muestra el resumen del último procesamiento"
- "¿Qué órdenes fallaron?"
- "Ejecuta el agente y muestra resultados"
- "Verifica los logs para errores"
```

---

## 📞 Soporte

- **Archivo Principal**: `agent.py`
- **Configuración**: `config.py`
- **Logs**: `logs/proceso.log`
- **Reporte**: `data/reporte_final.xlsx`
