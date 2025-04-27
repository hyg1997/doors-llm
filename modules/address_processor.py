import re

class AddressProcessor:
    @staticmethod
    def preprocess_address(address):
        pattern = r'([a-zA-Z]+)(\d+)'
        match = re.search(pattern, address)
        if match:
            text = match.group(1)
            number = match.group(2)
            
            text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
            text = ' '.join(re.findall('[A-Z][^A-Z]*', text)) if text.isupper() else text
            
            return f"{text} {number}"
        return address