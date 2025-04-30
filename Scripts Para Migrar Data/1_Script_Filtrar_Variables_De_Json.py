import json
import difflib
import os

# Función para filtrar una única variable de un diccionario JSON, incluyendo siempre el campo '_time' si está presente
def filtrar_una_variable(json_data, variable, umbral=0.8):
    json_filtrado = {}

    # Incluir el campo '_time' si está disponible
    if '_time' in json_data:
        json_filtrado['_time'] = json_data['_time']

    # Filtrar la variable solicitada
    if variable in json_data:
        json_filtrado[variable] = json_data[variable]
    else:
        # Buscar coincidencias cercanas
        coincidencias = difflib.get_close_matches(variable, json_data.keys(), n=1, cutoff=umbral)
        if coincidencias:
            print(f"Advertencia: '{variable}' no encontrada. ¿Quizás quisiste decir: {coincidencias[0]}?")
            json_filtrado[coincidencias[0]] = json_data[coincidencias[0]]
        else:
            print(f"Advertencia: '{variable}' no encontrada y no hay coincidencias.")
    
    return json_filtrado

# Función para procesar múltiples archivos JSON y generar un archivo por cada variable filtrada
def procesar_json_por_variable(rutas_json, variables_necesarias, directorio_salida='json_filtrados\ACB 3WA Principal'):
    # Crear el directorio de salida si no existe
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)

    for ruta_json in rutas_json:
        # Cargar el JSON desde el archivo
        with open(ruta_json, 'r') as archivo:
            datos = json.load(archivo)

        # Obtener el nombre del archivo original sin extensión
        nombre_archivo_base = os.path.splitext(os.path.basename(ruta_json))[0]

        # Filtrar por cada variable en la lista de variables necesarias
        for variable in variables_necesarias:
            if isinstance(datos, list):
                # Si los datos son una lista, filtrar cada elemento de la lista
                json_filtrado = [filtrar_una_variable(item, variable) for item in datos]
            else:
                # Si es un diccionario (objeto), filtrar directamente
                json_filtrado = filtrar_una_variable(datos, variable)

            # Verificar si el JSON filtrado contiene algo más que solo el campo '_time'
            if any(key != '_time' for item in json_filtrado for key in item.keys()):
                # Guardar el JSON filtrado para esta variable en un nuevo archivo
                ruta_variable_filtrada = os.path.join(directorio_salida, f'{nombre_archivo_base}_{variable}.json')
                with open(ruta_variable_filtrada, 'w') as archivo_filtrado:
                    json.dump(json_filtrado, archivo_filtrado, indent=4)

                print(f"Archivo JSON filtrado para '{variable}' guardado en: {ruta_variable_filtrada}")
            else:
                print(f"No se generó archivo para '{variable}' ya que solo contiene '_time'.")

# Lista de rutas de archivos JSON a procesar
rutas_json = [
r"C:\Users\z00517wf\Downloads\prueba\ACB 3WA Principal\Otros_Interruptor_principal_20240327-220600000_20240331-060000000.json",
r"C:\Users\z00517wf\Downloads\prueba\ACB 3WA Principal\Otros_Interruptor_principal_20240101-060000000_20240215-060000000.json",
r"C:\Users\z00517wf\Downloads\prueba\ACB 3WA Principal\Otros_Interruptor_principal_20240108-044000000_20240215-060000000.json",
r"C:\Users\z00517wf\Downloads\prueba\ACB 3WA Principal\Otros_Interruptor_principal_20240115-072900000_20240215-060000000.json",
r"C:\Users\z00517wf\Downloads\prueba\ACB 3WA Principal\Otros_Interruptor_principal_20240222-044000000_20240331-060000000.json",
r"C:\Users\z00517wf\Downloads\prueba\ACB 3WA Principal\Otros_Interruptor_principal_20240229-032000000_20240331-060000000.json",
r"C:\Users\z00517wf\Downloads\prueba\ACB 3WA Principal\Otros_Interruptor_principal_20240122-061300000_20240215-060000000.json",
r"C:\Users\z00517wf\Downloads\prueba\ACB 3WA Principal\Otros_Interruptor_principal_20240307-020100000_20240331-060000000.json",
r"C:\Users\z00517wf\Downloads\prueba\ACB 3WA Principal\Otros_Interruptor_principal_20240129-045400000_20240215-060000000.json",
r"C:\Users\z00517wf\Downloads\prueba\ACB 3WA Principal\Otros_Interruptor_principal_20240205-033400000_20240215-060000000.json",
r"C:\Users\z00517wf\Downloads\prueba\ACB 3WA Principal\Otros_Interruptor_principal_20240314-004100000_20240331-060000000.json",
r"C:\Users\z00517wf\Downloads\prueba\ACB 3WA Principal\Otros_Interruptor_principal_20240212-021400000_20240215-060000000.json",
r"C:\Users\z00517wf\Downloads\prueba\ACB 3WA Principal\Otros_Interruptor_principal_20240320-232600000_20240331-060000000.json"
]

# Lista de variables que necesitas filtrar
variables_necesarias = [
"Estado_breaker",
"Razon_ultimo_disparo"
"ETU_defectuoso",
"Mantenimiento_ETU_requerido",
"Inspeccion_ETU_requerido",
"Limite_ETU_temperatura",
"Falla_corriente_L1",
"Falla_corriente_L2",
"Falla_corriente_L3",
"Falla_corriente_N",
"Mantenimiento_contactos_requerido",
"Sobrecarga_L1",
"Sobrecarga_L2",
"Sobrecarga_L3",
"Falla_tierra",
"Manteniento_breaker_requerido",
"Disparos_LT"
"Disparos_ST",
"Disparos_INST",
"Disparos_GF",
"Disparos_RP",
"Cantidad_ciclos_electricos",
"Cantidad_ciclos_mecanicos",
"Voltaje_L1_N",
"Voltaje_L2_N",
"Voltaje_L3_N",
"Corriente_L1",
"Corriente_L2",
"Corriente_L3",
"Energia",
"Energia_exportada",
"Temperatura_breaker",
"Temperatura_BSS"



]

# Procesar los archivos JSON y generar un archivo por cada variable filtrada
procesar_json_por_variable(rutas_json, variables_necesarias)
