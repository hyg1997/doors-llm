import os
from dotenv import load_dotenv
from modules.address_validator import AddressValidator
from modules.address_processor import AddressProcessor

load_dotenv()

def main():
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file")
        return
    
    processor = AddressProcessor()
    validator = AddressValidator(api_key)
    
    while True:
        address = input("\nPlease enter a text containing an address (or 'exit' to quit): ")
        
        if address.lower() == 'exit':
            break

        processed_address = processor.preprocess_address(address)
        formated_address = validator.validate_and_format_address(processed_address)

        if not formated_address:
            print("No valid address found.")
            continue

        print(f"Formatted Address: {formated_address}")

if __name__ == "__main__":
    main()