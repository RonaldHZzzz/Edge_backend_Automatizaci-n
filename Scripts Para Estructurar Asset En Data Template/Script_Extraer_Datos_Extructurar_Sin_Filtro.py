import requests
import json

#formato para el diccionaro de datos del flow (Variable Data Template)
def extract_data_from_api(device_data):
   
    data = {
        "ACB 3WA": {
            "Assets": {
                device_data["item_id"]: device_data["item_name"]
            },
            "Variables": {}
        }
    }

    for i, display_name in enumerate(device_data["display_names"]):
        #traducir a español
       
        
        data["ACB 3WA"]["Variables"][str(0 + i)] = {
            "type": "LReal","name": {"en": display_name, "es": display_name}
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

    api_url = input("Ingrese la API de tu medidor: ")
    data = extract_data(api_url)

    if data:
        formatted_data = extract_data_from_api(data)
        
        save_path="C:\\Users\z00517wf\\Downloads\\cosas de ronald_xd\\cosas de ronald_xd\\industrial edge\\SCRIPTS\\data_prueba.json"
        try:

        # Guardar los datos en un archivo JSON con el formato deseado
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(formatted_data["ACB 3WA"], f, ensure_ascii=False)  # Guardamos 
        except Exception as e:

            print(f"Datos guardados en {save_path}")
    else:
        print("No se encontraron datos.")

if __name__ == "__main__":
    main()