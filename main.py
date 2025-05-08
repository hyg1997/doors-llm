from modules.address_validator import AddressValidator
from modules.address_processor import AddressProcessor

def main():
    processor = AddressProcessor()
    validator = AddressValidator()
    
    while True:
        print("\nOpciones:")
        print("1. Validar dirección")
        print("2. Ver todas las direcciones en la base de datos")
        print("3. Salir")
        
        option = input("\nSeleccione una opción (1-3): ")
        
        if option == "1":
            address = input("\nIngrese una dirección: ")
            processed_address = processor.preprocess_address(address)
            formatted_address = validator.validate_and_format_address(processed_address)
            print(f"\nDirección formateada: {formatted_address}")
            
        elif option == "2":
            addresses = validator.get_all_addresses()
            print("\nDirecciones en la base de datos:")
            for i, addr in enumerate(addresses, 1):
                print(f"{i}. {addr['direccion']} (score: {addr['score']:.4f})")
                
        elif option == "3":
            break
        else:
            print("\nOpción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()