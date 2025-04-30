import os

# Función para unir archivos de una carpeta específica
def combinar_archivos(carpeta_origen, archivo_salida):
    with open(archivo_salida, 'w') as outfile:
        for filename in os.listdir(carpeta_origen):
            if filename.endswith('.txt'):
                file_path = os.path.join(carpeta_origen, filename)
                print(f'Procesando {file_path}...')
                with open(file_path, 'r') as infile:
                    outfile.write(f'Archivo: {filename}\n')
                    outfile.write(infile.read())
                    outfile.write('\n')  # Añadir nueva línea entre archivos
    print(f'Archivos de {carpeta_origen} combinados en {archivo_salida}')

# Lista de carpetas a procesar
carpetas = [
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Falla_corriente_N",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Inspeccion_ETU_requerido",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Limite_ETU_temperatura",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Mantenimiento_contactos_requerido",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Mantenimiento_ETU_requerido",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Sobrecarga_L1",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Falla_tierra",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Voltaje_L2_N",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Cantidad_ciclos_electricos",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Cantidad_ciclos_mecanicos",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Corriente_L1",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Corriente_L2",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Corriente_L3",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Disparos_GF",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Disparos_INST",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Disparos_RP",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Energia",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Energia_exportada",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Manteniento_breaker_requerido",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Sobrecarga_L2",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Sobrecarga_L3",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Temperatura_breaker",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Temperatura_BSS",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Voltaje_L1_N",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Voltaje_L3_N",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Estado_breaker",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Falla_corriente_L1",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Falla_corriente_L2",
r"C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Falla_corriente_L3"
]

# Ruta donde se guardarán los archivos combinados
carpeta_destino = r'C:\Users\z00517wf\Downloads\prueba\variablestxt\ACB 3WA Principal\Combinados'

# Verificar si la carpeta de destino existe, si no, crearla
if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

# Procesar cada carpeta
for carpeta in carpetas:
    # Obtener el nombre de la carpeta para usarlo en el nombre del archivo de salida
    nombre_carpeta = os.path.basename(carpeta)
    archivo_salida = os.path.join(carpeta_destino, f'{nombre_carpeta}_combinado.txt')
    
    # Combinar archivos en la carpeta
    combinar_archivos(carpeta, archivo_salida)

print(f'Archivos combinados guardados en {carpeta_destino}')
