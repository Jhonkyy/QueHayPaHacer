from interfaces.consola import InterfazConsola
from models.sistema import Sistema

def main():
    sistema = Sistema()
    interfaz = InterfazConsola(sistema)
    interfaz.mostrar_menu_principal()

if __name__ == "__main__":
    main()