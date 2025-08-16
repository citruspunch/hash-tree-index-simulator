"""
Interfaz de línea de comandos para el simulador de hash extensible
"""

from directory import Directory
from config import MESSAGES, MENU_OPTIONS, MIN_KEY_VALUE, MAX_KEY_VALUE


class ExtensibleHashCLI:
    def __init__(self):
        self.directory = Directory()
    
    def show_welcome(self):
        """Muestra el mensaje de bienvenida"""
        print(MESSAGES['WELCOME'])
        print(MESSAGES['HASH_FUNCTION'])
        print(MESSAGES['KEY_RANGE'])
        print(MESSAGES['BUCKET_CAPACITY'])
    
    def show_menu(self):
        """Muestra el menú principal"""
        print(f"\n--- Menú Principal ---")
        print("1. Insertar clave (1-100)")
        print("2. Eliminar clave")
        print("3. Buscar clave")
        print("4. Imprimir configuración del índice")
        print("5. Salir")
    
    def handle_insert(self):
        """Maneja la opción de insertar clave"""
        try:
            key = int(input(f"Ingrese la clave a insertar ({MIN_KEY_VALUE}-{MAX_KEY_VALUE}): "))
            success, message = self.directory.insert(key)
            print(f"✓ {message}" if success else f"✗ {message}")
            if success:
                self.directory.print_status()
        except ValueError:
            print(MESSAGES['INVALID_NUMBER'])
    
    def handle_delete(self):
        """Maneja la opción de eliminar clave"""
        try:
            key = int(input("Ingrese la clave a eliminar: "))
            success, message = self.directory.delete(key)
            print(f"✓ {message}" if success else f"✗ {message}")
            if success:
                self.directory.print_status()
        except ValueError:
            print(MESSAGES['INVALID_NUMBER'])
    
    def handle_search(self):
        """Maneja la opción de buscar clave"""
        try:
            key = int(input("Ingrese la clave a buscar: "))
            found = self.directory.search(key)
            print(f"✓ Clave {key} encontrada" if found else f"✗ Clave {key} no encontrada")
        except ValueError:
            print(MESSAGES['INVALID_NUMBER'])
    
    def handle_print_status(self):
        """Maneja la opción de imprimir configuración"""
        self.directory.print_status()
    
    def run(self):
        """Ejecuta el bucle principal de la CLI"""
        self.show_welcome()
        
        while True:
            self.show_menu()
            
            try:
                opcion = input("\nSeleccione una opción (1-5): ").strip()
                
                if opcion == MENU_OPTIONS['INSERT']:
                    self.handle_insert()
                elif opcion == MENU_OPTIONS['DELETE']:
                    self.handle_delete()
                elif opcion == MENU_OPTIONS['SEARCH']:
                    self.handle_search()
                elif opcion == MENU_OPTIONS['PRINT']:
                    self.handle_print_status()
                elif opcion == MENU_OPTIONS['EXIT']:
                    print(MESSAGES['GOODBYE'])
                    break
                else:
                    print(MESSAGES['INVALID_OPTION'])
            
            except KeyboardInterrupt:
                print(f"\n{MESSAGES['GOODBYE']}")
                break
            except Exception as e:
                print(f"✗ Error inesperado: {e}")
