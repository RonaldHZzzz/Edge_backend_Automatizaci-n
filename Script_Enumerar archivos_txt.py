import os

def enumerate_files_in_folders(folder_paths):
    for folder_path in folder_paths:
        if os.path.exists(folder_path):
            print(f"Procesando carpeta: {folder_path}")
            # Obtener lista de archivos .txt en la carpeta
            txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
            
            # Enumerar los archivos y renombrarlos con un número al inicio
            for index, file_name in enumerate(txt_files, start=1):
                old_file_path = os.path.join(folder_path, file_name)
                new_file_name = f"{index}_{file_name}"
                new_file_path = os.path.join(folder_path, new_file_name)
                
                # Renombrar archivo
                os.rename(old_file_path, new_file_path)
                print(f'Renombrado: {old_file_path} -> {new_file_path}')
        else:
            print(f"La carpeta no existe: {folder_path}")

# Ejemplo de uso
folder_paths = [
'variablestxt\ACB 3WA Principal\Voltaje_L2_N'
]

enumerate_files_in_folders(folder_paths)

