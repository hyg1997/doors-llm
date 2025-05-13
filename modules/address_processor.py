import re
import unicodedata

class AddressProcessor:
    @staticmethod
    def preprocess_address(address):
        if not isinstance(address, str):
            return ""
        
        address = AddressProcessor._normalize_chars(address.lower())
        
        address = re.sub(r'\s+', ' ', address)
        address = address.strip()
        
        address = re.sub(r'([a-z])(\d)', r'\1 \2', address)
        address = re.sub(r'(\d)([a-z])', r'\1 \2', address)
        
        return address
    
    @staticmethod
    def _normalize_chars(text):
        text = ''.join(c for c in unicodedata.normalize('NFD', text)
                      if unicodedata.category(c) != 'Mn')
        
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        
        return text