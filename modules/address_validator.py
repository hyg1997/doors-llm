from langchain.vectorstores import Chroma
from .vector_store import VectorStore
import re

class AddressValidator:
    def __init__(self, csv_path="./data/1641279574.csv"):
        self.device = "cpu"
        self.vector_store_manager = VectorStore()
        
        try:
            # Instead of creating from CSV again, just load the existing collection
            self.vector_store = Chroma(
                client=self.vector_store_manager.client,
                collection_name="addresses",
                embedding_function=self.vector_store_manager.embeddings,
                persist_directory=self.vector_store_manager.persist_directory
            )
        except Exception as e:
            raise Exception(f"Error al cargar la base de datos vectorial: {str(e)}")

    def _normalize_address(self, address):
        if not isinstance(address, str):
            return ""
            
        prefixes = {
            r'\b(jr|jiron|jirón|jr\.|jiron\.|jirón\.)\b': 'Jr.',
            r'\b(av|avda|avenida|av\.|avda\.)\b': 'Av.',
            r'\b(ca|calle|ca\.)\b': 'Calle',
            r'\b(psje|pasaje|psj|psj\.)\b': 'Pasaje',
            r'\b(urb|urbanizacion|urbanización|urb\.)\b': 'Urb.'
        }
        
        normalized = address.lower()
        
        for pattern, replacement in prefixes.items():
            normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)
        
        words = normalized.split()
        skip_words = {'de', 'del', 'la', 'las', 'los', 'y', 'e', 'el'}
        
        normalized_words = []
        for i, word in enumerate(words):
            if word.lower() in skip_words and i > 0:
                normalized_words.append(word.lower())
            else:
                normalized_words.append(word.capitalize())
                
        return ' '.join(normalized_words)
    
    def validate_and_format_address(self, address):
        try:
            normalized_input = self._normalize_address(address)
            results = self.vector_store.similarity_search_with_score(
                normalized_input,
                k=3
            )
            
            if not results:
                return {
                    "contains_address": False,
                    "formatted_address": "",
                    "explanation": f"No se encontró una dirección similar a '{address}'"
                }
            
            best_match = None
            best_score = float('inf')
            for doc, score in results:
                candidate = self._normalize_address(str(doc))
                text_similarity = self._calculate_text_similarity(normalized_input, candidate)
                combined_score = score * (1 - text_similarity)
                
                if combined_score < best_score:
                    best_score = combined_score
                    best_match = candidate
            
            if best_score < 0.7:
                number = next((part for part in address.split() if part.isdigit()), "")
                if number and number not in best_match:
                    best_match = f"{best_match} {number}"
                
                return {
                    "contains_address": True,
                    "formatted_address": best_match,
                    "explanation": f"La dirección '{address}' ha sido normalizada según referencias históricas"
                }
            else:
                basic_format = self._normalize_address(address)
                return {
                    "contains_address": True,
                    "formatted_address": basic_format,
                    "explanation": f"No se encontró una coincidencia exacta. Se ha aplicado un formato básico a '{address}'"
                }
            
        except Exception as e:
            return {
                "contains_address": False,
                "formatted_address": "",
                "explanation": f"Error al procesar la dirección: {str(e)}"
            }
    
    def _calculate_text_similarity(self, text1, text2):
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        return intersection / union if union > 0 else 0
    
    def get_all_addresses(self):
        return self.vector_store_manager.get_all_addresses(
            self.vector_store._collection,
            self._normalize_address
        )