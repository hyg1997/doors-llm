from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import pandas as pd
import os
import chromadb

class VectorStore:
    def __init__(self, persist_directory="./data/vector_db"):
        self.persist_directory = persist_directory
        if not os.path.exists(persist_directory):
            os.makedirs(persist_directory, exist_ok=True)
            
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002"
        )
        self.client = chromadb.PersistentClient(path=persist_directory)
        
    def create_from_csv(self, csv_path):
        """Crea una base de datos vectorial a partir de un archivo CSV"""
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"El archivo CSV no existe en la ruta: {csv_path}")
            
        df = pd.read_csv(csv_path)
        addresses = []
        
        for _, row in df.iterrows():
            if isinstance(row['Direccion'], str):
                addresses.append(row['Direccion'])
        
        return Chroma.from_texts(
            texts=addresses,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            client=self.client,
            collection_name="addresses"
        )
        
    def get_all_addresses(self, collection):
        """Obtiene todas las direcciones almacenadas"""
        try:
            results = collection.get()
            addresses = []
            if results['documents']:
                for doc in results['documents']:
                    addresses.append(doc)
            return addresses
            
        except Exception as e:
            print(f"Error al obtener las direcciones: {str(e)}")
            return []