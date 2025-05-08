from modules.address_validator import AddressValidator
from modules.vector_store import VectorStore
import shutil
import os


def clean_database(persist_directory="./data/vector_db"):
    """
    Limpia la base de datos vectorial eliminando todos los archivos
    """
    try:
        if os.path.exists(persist_directory):
            shutil.rmtree(persist_directory)
            print("Base de datos eliminada exitosamente.")
    except Exception as e:
        print(f"Error al limpiar la base de datos: {str(e)}")

def populate_database(csv_path="./data/1641279574.csv", clean=False):
    """
    Función para poblar la base de datos vectorial con direcciones desde un CSV
    
    Args:
        csv_path (str): Ruta al archivo CSV con las direcciones
        clean (bool): Si es True, limpia la base de datos antes de poblarla
    """
    persist_directory = "./data/vector_db"
    
    if clean:
        clean_database()
    
    os.makedirs(persist_directory, exist_ok=True)
    
    vector_store = VectorStore()
    
    try:
        if clean or not os.path.exists(os.path.join(persist_directory, "chroma.sqlite3")):
            validator = AddressValidator()
            vector_store.create_from_csv(
                csv_path, 
                validator._normalize_address
            )
            print("Base de datos poblada exitosamente.")
        else:
            print("La base de datos ya existe, no es necesario volver a poblarla.")
    except Exception as e:
        print(f"Error al poblar la base de datos: {str(e)}")

if __name__ == "__main__":
    populate_database(clean=True)