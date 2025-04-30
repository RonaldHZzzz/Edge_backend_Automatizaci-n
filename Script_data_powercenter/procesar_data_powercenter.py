import pandas as pd
import glob
import os
import re
from datetime import datetime, timezone

def extraer_metadatos(primera_linea):
    """Extrae el nombre del dispositivo y el dataPoint del encabezado completo"""
    device_match = re.search(r'device="([^"]+)"', primera_linea)
    datapoint_match = re.search(r'dataPoint="([^"]+)"', primera_linea)

    device = device_match.group(1) if device_match else "device_unknown"
    datapoint = datapoint_match.group(1) if datapoint_match else "dataPoint_unknown"

    # Reemplazar caracteres no permitidos en nombres de archivo
    device = re.sub(r"[^\w\s-]", "", device).replace(" ", "_")
    datapoint = re.sub(r"[^\w\s-]", "", datapoint).replace(" ", "_")

    return device, datapoint

def procesar_archivos(archivos_csv, carpeta_salida="procesados"):
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    for archivo in archivos_csv:
        with open(archivo, "r", encoding="utf-8") as f:
            primera_linea = f.readline().strip()  # Leer la línea con metadatos

        device, datapoint = extraer_metadatos(primera_linea)
        df = pd.read_csv(archivo, sep=";", skiprows=1)

        # Detectar la columna de valor: puede ser "Valor absoluto" o "Valor"
        posibles_nombres = ["Valor absoluto", "Valor"]
        columna_valor = next((col for col in posibles_nombres if col in df.columns), None)

        if not columna_valor:
            print(f"Columna de valor no encontrada en {archivo}")
            continue

        # Filtrar filas sin datos en la columna de valor
        df = df[df[columna_valor].notna()]

        # Reemplazar comas por puntos y convertir a float
        df[columna_valor] = df[columna_valor].astype(str).str.replace(",", ".").astype(float)

        # Crear nueva columna convertida
        df["Convertido"] = df[columna_valor] / 1000

        # Generar nombre del archivo de salida
        nombre_salida = f"{device}_{datapoint}.txt"
        ruta_salida = os.path.join(carpeta_salida, nombre_salida)

        with open(ruta_salida, "w", encoding="utf-8") as txt_file:
            txt_file.write(f"name:{nombre_salida}\ttype:Double\n")

            for _, row in df.iterrows():
                try:
                    # Convertir la fecha al formato UTC con milisegundos
                    fecha_obj = datetime.strptime(row["Fecha/hora"], "%Y-%m-%dT%H:%M:%S%z")
                    timestamp = fecha_obj.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
                except Exception as e:
                    print(f"Error en la fecha en archivo {archivo}: {e}")
                    continue

                valor = row["Convertido"]
                txt_file.write(f"{timestamp}\t{valor:.4f}\t192\n")

        print(f"Archivo procesado: {ruta_salida}")

# Buscar archivos CSV en la carpeta actual
archivos_csv = glob.glob("*.csv")

# Procesar los archivos encontrados
procesar_archivos(archivos_csv)
