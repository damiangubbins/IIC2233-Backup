from entities import Item, Usuario
from loader import cargar_items
from pretty_print import *


def menu(user: Usuario):
    while True:
        print_opciones_menu()
        opcion = input("> ")

        if opcion == "a":
            ...
        elif opcion == "b":
            ...
        elif opcion == "c":
            print_canasta(user)
        elif opcion == "d":
            print_usuario(user)
            print_items(cargar_items())
        elif opcion == "e":
            print_salida()
            break
        else:
            print_opcion_invalida()


if __name__ == "__main__":
    user = Usuario(False, [], 0)
    menu(user)
