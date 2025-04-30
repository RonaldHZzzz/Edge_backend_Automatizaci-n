import requests
import json

# Formato para el diccionario de datos del flow (Variable Data Template)
def extract_data_from_api(device_data, filter_names):
    data = {
        "ACB 3WA": {
            "Assets": {
                device_data["item_id"]: device_data["item_name"]
            },
            "Variables": {}
        }
    }

    for i, display_name in enumerate(device_data["display_names"]):
        # Solo agregar las variables que estén en el filtro
        if display_name in filter_names:
            data["ACB 3WA"]["Variables"][str(0+i)] = {
                "type": "LReal", "name": {"en": display_name, "es": display_name}
            }

    return data

def extract_data(api_url):
    try:
        response = requests.get(api_url).json()
        return {
            "item_id": response["item_id"],
            "item_name": response["item_name"],
            "display_names": [item["display_name"] for item in response["_embedded"]["item"]]
        }
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos: {e}")
        return {}

def main():
    """Función principal para manejar la interacción con la API y la extracción de datos."""

    api_url = input("Ingrese la URL de la API de tu medidor: ")
    data = extract_data(api_url)

    if data:
        # Lista de nombres de variables a filtrar directamente en el código
        filter_names = [ "State of breaker",
    "Reason of trip",
    "Number of temperature trips",
    "Number of G trips",
    "Number of I trips",
    "Number of L trips",
    "Number of N trips",
    "Number of S trips",
    "Main contact state",
    "Operating hours counter",
    "Breaker health",
    "Current L1",
    "Current L2",
    "Current L3",
    "Voltage L1-N",
    "Voltage L2-N",
    "Voltage L3-N",
    "Voltage L1-L2",
    "Voltage L2-L3",
    "Voltage L3-L1",
    "Total Active Power",
    "Total Reactive Power Qtot",
    "Total Apparent Power",
    "Total Power Factor",
    "Active energy imported",
    "Active energy exported"]  # Nombres de ejemplo

        formatted_data = extract_data_from_api(data, filter_names)

        # Guardar los datos en un archivo JSON con el formato deseado
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(formatted_data["ACB 3WA"], f, ensure_ascii=False)

        print("Datos guardados en data.json")
    else:
        print("No se encontraron datos.")

if __name__ == "__main__":
    main()
