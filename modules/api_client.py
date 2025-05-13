import requests
from requests.exceptions import RequestException
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional

class ApiClient:
    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv('API_BASE_URL', 'https://ue-api.urbanoexpress.com.pe')
        
    def get_addresses(self) -> Optional[List[Dict]]:
        """
        Obtiene las direcciones desde el endpoint externo
        
        Returns:
            Lista de direcciones o None si hay error
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
                'Accept': 'application/json',
                'Origin': 'https://ue-api.urbanoexpress.com.pe',
                'Referer': 'https://ue-api.urbanoexpress.com.pe/'
            }
            
            response = requests.get(
                f"{self.base_url}/geomap/api/crontab/externo-guias",
                verify=True,
                headers=headers
            )
            
            response.raise_for_status()
            
            data = response.json()
            if data.get('sql_err') == 0 and 'data' in data:
                return data['data']
            
            print(f"Error en la respuesta del API: {data.get('sql_msn', 'Sin mensaje de error')}")
            return None
            
        except requests.exceptions.Timeout:
            print("Error: Tiempo de espera agotado al conectar con el API")
            return None
        except requests.exceptions.SSLError:
            print("Error: Problema con la verificación SSL")
            return None
        except requests.exceptions.ConnectionError as e:
            print(f"Error de conexión: No se pudo conectar al API - {str(e)}")
            return None
        except RequestException as e:
            print(f"Error al realizar la petición HTTP: {str(e)}")
            return None
        except Exception as e:
            print(f"Error inesperado al obtener direcciones del API: {str(e)}")
            return None