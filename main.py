from src import cargar_excel, generar_test

def main():
    print("=== Bienvenido al Generador de Exámenes ===")
    cargar_excel.importar_preguntas()
    generar_test.menu_test()

if __name__ == "__main__":
    main()