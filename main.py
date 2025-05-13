from modules.address_validator import AddressValidator
from modules.address_processor import AddressProcessor
from modules.api_client import ApiClient

def main():
    processor = AddressProcessor()
    validator = AddressValidator()
    api_client = ApiClient()
    
    while True:
        print("\nOpciones:")
        print("1. Validar dirección")
        print("2. Ver todas las direcciones en la base de datos")
        print("3. Validar direcciones del API")
        print("4. Salir")
        
        option = input("\nSeleccione una opción (1-4): ")
        
        if option == "1":
            address = input("\nIngrese una dirección: ")
            print("\nResultados de validación:")
            print(f"\nDirección Original: {address}")
            processed_address = processor.preprocess_address(address)
            validation_result = validator.validate_and_format_address(processed_address)
            print(f"Result: {validation_result['formatted_address']}")
            print(f"Explicación: {validation_result['explanation']}")
            print(f"Porcentaje: {validation_result['similarity_percentage']}")
            
        elif option == "2":
            addresses = validator.get_all_addresses()
            print("\nDirecciones en la base de datos:")
            for i, addr in enumerate(addresses, 1):
                print(f"{i}. {addr}")
                
        elif option == "3":
            print("\nObteniendo y validando direcciones del API...")
            addresses = api_client.get_addresses()
            if addresses:
                print("\nResultados de validación:")
                for i, addr in enumerate(addresses, 1):
                    original_address = addr['direccion'].strip()
                    processed_address = processor.preprocess_address(original_address)
                    validation_result = validator.validate_and_format_address(processed_address)
                    
                    print(f"\n{i}. Dirección Original: {original_address}")
                    print(f"   Ciudad: {addr['ciu_nombre']}")
                    print(f"   Provincia: {addr['prv_nombre']}")
                    print(f"   Departamento: {addr['dep_nombre']}")
                    if addr['referecia']:
                        print(f"   Referencia: {addr['referecia']}")
                    print(f"   Resultado: {validation_result['formatted_address']}")
                    print(f"   Explicación: {validation_result['explanation']}")
                    print(f"   Porcentaje: {validation_result['similarity_percentage']}")
            else:
                print("\nNo se pudieron obtener direcciones del API")
                
        elif option == "4":
            break
        else:
            print("\nOpción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()