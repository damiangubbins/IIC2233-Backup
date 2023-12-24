import os
import sys

import extras
from imprimir_tablero import imprimir_tablero
from tablero import Tablero


def menu_base():

    return f'''
Hola {USER_NAME}!

*** Menú de Acciones ***

[1] Mostrar tablero
[2] Limpiar tablero
[3] Solucionar tablero
[4] Salir del programa

Indique su opción (1, 2, 3 o 4)
'''


def wait():
    input("Presione ENTER para volver al menú...")
    os.system("cls")


def menu():

    while True:
        print(menu_base())
        opcion = input("> ")

        os.system("cls")

        match opcion:
            case "1":
                imprimir_tablero(tablero_oficial.tablero)
                wait()
            case "2":
                tablero_oficial.limpiar()
                print(extras.print_consola("Tablero limpiado"))
                wait()
            case "3":
                tablero_oficial.solucionar()
                wait()
            case "4":
                print(extras.print_consola(f"Adiós {USER_NAME}!"))
                sys.exit()
            case _:
                print(extras.print_consola("Opción inválida"))
                wait()


if __name__ == "__main__":

    try:
        USER_NAME = sys.argv[1]
        TABLERO = sys.argv[2]
    except IndexError:
        print(extras.print_consola("Faltan argumentos"))
        sys.exit()

    CHECK = True

    tableros = extras.leer_tableros_txt()

    if not USER_NAME.isalpha() or len(USER_NAME) < 4:
        print(extras.print_consola("Nombre de usuario inválido"))
        CHECK = False

    if TABLERO not in tableros.keys():
        print(extras.print_consola("El tablero no existe"))
        CHECK = False

    if CHECK:
        tablero_oficial = Tablero(extras.txt_a_list(TABLERO))
        menu()
    else:
        sys.exit()
