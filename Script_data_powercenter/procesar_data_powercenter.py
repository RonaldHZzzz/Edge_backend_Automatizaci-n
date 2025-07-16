import pandas as pd
import glob
import os
import re
from datetime import datetime, timezone

def extraer_metadatos(primera_linea):
    try:
        device_match = re.search(r'device="([^"]+)"', primera_linea)
        datapoint_match = re.search(r'dataPoint="([^"]+)"', primera_linea)

        device = device_match.group(1) if device_match else "device_unknown"
        datapoint = datapoint_match.group(1) if datapoint_match else "dataPoint_unknown"

        # Sanitizar nombres para archivos
        device = re.sub(r"[^\w\s-]", "", device).replace(" ", "_").strip()[:50]
        datapoint = re.sub(r"[^\w\s-]", "", datapoint).replace(" ", "_").strip()[:50]

        print(f"[INFO] Dispositivo: {device}, DataPoint: {datapoint}")
        return device, datapoint
    except Exception as e:
        print(f"[ERROR] Error extrayendo metadatos: {str(e)}")
        return "device_unknown", "dataPoint_unknown"

def procesar_archivos(archivos_csv, carpeta_salida="procesados"):
    try:
        os.makedirs(carpeta_salida, exist_ok=True)
    except OSError as e:
        print(f"[ERROR] No se pudo crear carpeta de salida: {str(e)}")
        return

    for archivo in archivos_csv:
        print(f"\n{'='*50}\n[PROCESANDO ARCHIVO] {archivo}\n{'='*50}")

        try:
            with open(archivo, "r", encoding="utf-8", errors='replace') as f:
                primera_linea = f.readline().strip()
        except Exception as e:
            print(f"[ERROR] No se pudo leer el archivo: {str(e)}")
            continue

        try:
            device, datapoint = extraer_metadatos(primera_linea)
        except Exception as e:
            print(f"[ERROR] Fallo en metadatos: {str(e)}")
            device, datapoint = "unknown", "unknown"

        try:
            df = pd.read_csv(
                archivo,
                sep=";",
                skiprows=1,
                on_bad_lines='warn',
                engine='python',
                encoding='utf-8'
            )
        except Exception as e:
            print(f"[ERROR] Error leyendo CSV: {str(e)}")
            continue

        # Manejar diferentes nombres de columna para valores
        columna_valor = None
        for col in ["Valor absoluto", "Valor"]:
            if col in df.columns:
                columna_valor = col
                break
        
        if not columna_valor:
            print("[ERROR] No se encontró columna de valores (Valor absoluto/Valor)")
            continue

        # Validar columnas requeridas
        required_columns = {"Fecha/hora", columna_valor}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            print(f"[ERROR] Columnas faltantes: {', '.join(missing)}")
            continue

        # Procesar valores numéricos
        try:
            df = df[df[columna_valor].notna()]
            df[columna_valor] = (
                df[columna_valor]
                .astype(str)
                .str.replace(",", ".", regex=False)
                .str.strip()
            )
            df[columna_valor] = pd.to_numeric(df[columna_valor], errors="coerce")
            df = df[df[columna_valor].notna()]
            
            if df.empty:
                print("[ERROR] DataFrame vacío después de limpieza")
                continue
                
            # Conversión a kWh (dividir Wh entre 1000)
            df["Convertido"] = df[columna_valor] / 1000
        except Exception as e:
            print(f"[ERROR] Procesamiento numérico fallido: {str(e)}")
            continue

        # Generar archivo de salida
        nombre_salida = f"{device}_{datapoint}.txt".replace("__", "_")
        ruta_salida = os.path.join(carpeta_salida, nombre_salida)

        registros_exitosos = 0
        with open(ruta_salida, "w", encoding="utf-8") as txt_file:
            # Encabezado con tabulaciones
            txt_file.write(f"name:{nombre_salida}\ttype:Double\n")

            for _, row in df.iterrows():
                try:
                    fecha_str = row["Fecha/hora"]
                    
                    # Corregir formato de zona horaria (remover : en el offset)
                    fecha_str = re.sub(
                        r"([+-]\d{2}):(\d{2})$", 
                        r"\1\2", 
                        fecha_str
                    )
                    
                    # Convertir a datetime con offset
                    fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%dT%H:%M:%S%z")
                    utc_time = fecha_obj.astimezone(timezone.utc)
                    
                    # Formatear timestamp con milisegundos (3 decimales)
                    timestamp = utc_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
                    
                    # Formatear valor con 4 decimales
                    valor = round(row["Convertido"], 4)
                    
                    # CORRECCIÓN: Usar tabulaciones en lugar de espacios fijos
                    txt_file.write(f"{timestamp}\t{valor:.4f}\t192\n")
                    registros_exitosos += 1
                    
                except Exception as e:
                    print(f"[ERROR FECHA] {fecha_str} | Error: {str(e)}")

        print(f"\n[RESULTADO] Archivo: {nombre_salida}")
        print(f"Registros totales: {len(df)}")
        print(f"Registros exitosos: {registros_exitosos}")
        print(f"Errores de fecha: {len(df) - registros_exitosos}")

if __name__ == "__main__":
    try:
        archivos = glob.glob("*.csv")
        if not archivos:
            print("[INFO] No se encontraron archivos CSV en el directorio actual")
        else:
            procesar_archivos(archivos)
            print("\nProceso completado. Revise la carpeta 'procesados'")
    except Exception as e:
        print(f"[ERROR GLOBAL] {str(e)}")
    finally:
        input("\nPresione Enter para salir...")