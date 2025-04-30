📄 Documentación - Script de procesamiento de archivos CSV
🧩 Descripción
Este script automatiza el procesamiento de archivos .csv con datos de sensores (como medidores eléctricos), extrayendo metadatos, limpiando los datos y generando archivos .txt con formato estandarizado para su posterior uso.

🛠️ Requisitos
Python 3.x

Librerías necesarias:

pandas

glob

os

re

datetime

Puedes instalar pandas si no lo tienes:

bash
Copiar
Editar
pip install pandas
📁 Estructura esperada del archivo CSV
Primera línea: contiene los metadatos device="..." y dataPoint="...".

Desde la segunda línea: datos con al menos estas dos columnas:

Fecha/hora → en formato ISO (YYYY-MM-DDTHH:MM:SS±HH:MM)

Valor absoluto → valores numéricos (con coma como decimal)

⚙️ Qué hace el script
Lee todos los archivos .csv del directorio actual.

Extrae los metadatos del dispositivo y punto de datos desde la primera línea.

Lee el resto del archivo como DataFrame con pandas.

Limpia y convierte los valores numéricos.

Convierte los valores a otra escala (por defecto, divide entre 1000).

Convierte las fechas a formato UTC y genera un archivo .txt en la carpeta procesados/.

El formato de salida es:

pgsql
Copiar
Editar
name:nombre_archivo.txt	type:Double
2024-01-01T05:00:00.000Z	0.052	192
🚀 Cómo usarlo
Coloca el script en el mismo directorio donde están los archivos .csv.

Ejecuta el script:

bash
Copiar
Editar
python nombre_del_script.py
Se generará una carpeta procesados/ con los archivos .txt de salida.

Al finalizar, el script muestra un resumen de registros exitosos y errores.

📌 Notas importantes
Si los valores numéricos usan , como separador decimal, se convierten a . antes de procesarlos.

Las fechas se transforman correctamente a formato UTC (Z) para compatibilidad con sistemas internacionales.

Si faltan columnas o hay errores en la conversión, el archivo será omitido con un mensaje de advertencia.

