from langchain_chroma import Chroma
from .vector_store import VectorStore
from typing import Dict, List, Tuple

class AddressValidator:
    def __init__(self):
        """Initialize the AddressValidator with vector store configuration."""
        self.device = "cpu"
        self.vector_store_manager = VectorStore()
        
        try:
            self.vector_store = Chroma(
                client=self.vector_store_manager.client,
                collection_name="addresses",
                embedding_function=self.vector_store_manager.embeddings,
                persist_directory=self.vector_store_manager.persist_directory
            )
        except Exception as e:
            raise Exception(f"Error al cargar la base de datos vectorial: {str(e)}")

    def validate_and_format_address(self, address: str) -> Dict[str, any]:
        """
        Validate and format an address using vector similarity search.
        
        Args:
            address: The input address to validate and format
            
        Returns:
            Dictionary containing validation results with similarity percentage
        """
        try:
            if not self._is_valid_input(address):
                return self._create_error_response("La dirección ingresada es demasiado corta o inválida")
            
            results = self.vector_store.similarity_search_with_score(address, k=10)
            if not results:
                return self._create_error_response(f"No se encontró una dirección similar a '{address}'")
    
            filtered_results = self._process_similarity_results(address, results)
            if not filtered_results:
                return self._create_error_response(f"No se encontraron direcciones suficientemente similares a '{address}'")
    
            best_match, best_score = filtered_results[0]
            similarity_percentage = self._calculate_similarity_percentage(best_score)
            
            return {
                "contains_address": True,
                "formatted_address": best_match,
                "explanation": f"La dirección '{address}' ha sido normalizada según referencias históricas",
                "similarity_percentage": similarity_percentage
            }
                
        except Exception as e:
            return self._create_error_response(f"Error al procesar la dirección: {str(e)}")
    
    def _calculate_similarity_percentage(self, score: float) -> float:
        """Calculate similarity percentage from score."""
        return round((1 - score) * 100, 2)
    
    def _create_error_response(self, explanation: str) -> Dict[str, any]:
        """Create a standardized error response."""
        return {
            "contains_address": False,
            "formatted_address": "",
            "explanation": explanation,
            "similarity_percentage": 0.0
        }

    def _is_valid_input(self, address: str) -> bool:
        """Check if the input address is valid."""
        return bool(address and isinstance(address, str) and len(address.strip()) >= 3)
    
    def _process_similarity_results(self, address: str, results: List[Tuple]) -> List[Tuple[str, float]]:
        """Process and filter similarity search results."""
        filtered_results = []
        for doc, score in results:
            doc_address = str(doc.page_content) if hasattr(doc, 'page_content') else str(doc)
            text_similarity = self._calculate_text_similarity(address, doc_address)
            adjusted_score = score * (1 - text_similarity)
            filtered_results.append((doc_address, adjusted_score))
        
        return sorted(filtered_results, key=lambda x: x[1])
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity using Jaccard similarity."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        return intersection / union if union > 0 else 0
    
    def _create_error_response(self, explanation: str) -> Dict[str, any]:
        """Create a standardized error response."""
        return {
            "contains_address": False,
            "formatted_address": "",
            "explanation": explanation,
            "score": 1.0
        }

    def get_all_addresses(self) -> List[str]:
        """Retrieve all addresses from the vector store."""
        try:
            results = self.vector_store._collection.get()
            if not results or 'documents' not in results:
                return []
            
            return [doc for doc in results['documents'] if isinstance(doc, str)]
            
        except Exception as e:
            print(f"Error al obtener las direcciones: {str(e)}")
            return []