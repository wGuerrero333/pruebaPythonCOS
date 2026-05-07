import pandas as pd
# SE IMPORTA LA LIBRERIA PANDAS PARA LEER Y ESCRIBIR ARCHIVOS EXCEL
def leer_ordenes(ruta):
    return pd.read_excel(ruta)

def guardar_reporte(data, ruta):
    df = pd.DataFrame(data)
    df.to_excel(ruta, index=False)