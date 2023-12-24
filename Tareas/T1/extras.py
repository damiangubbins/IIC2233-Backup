"""
Funciones adicionales para facilitar el desarrollo y eficiencia del programa.
"""

import copy

import funciones
from pieza_explosiva import PiezaExplosiva


def print_consola(mensaje: str):
    """
    Imprime un (mensage: str) en un formato especial.
    """
    return f"\n{'-'*37}\n\n{mensaje.center(37)}\n\n{'-'*37}\n"


def leer_tableros_txt() -> dict:
    """
    Abre el archivo tableros.txt y guarda los tableros en un diccionario.
    """
    with open("tableros.txt", "r", encoding="utf-8") as file:
        tableros = file.readlines()
        tableros = [tablero.rstrip().split(",") for tablero in tableros]
        return {tablero[0]: tablero[1:] for tablero in tableros}


def txt_a_list(tablero: str) -> list:
    """
    Obtiene el tablero en tableros.txt a partir del nombre de un (tablero: str)

    Este es luego convertido a una lista legible para la clase Tablero.
    """
    tableros_dict = leer_tableros_txt()

    filas = int(tableros_dict[tablero][0])
    columnas = int(tableros_dict[tablero][1])
    tablero_str = tableros_dict[tablero][2:]

    tablero_mod = [[] for _ in range(filas)]

    for i, pieza in enumerate(tablero_str):
        tablero_mod[i//columnas].append(pieza)

    return tablero_mod


def tranformar_inversa(tablero: list) -> list:
    """
    Crea una copia de un (tablero: list) y des-instancia las piezas explosivas.

    list[PiezaExplosiva] -> list[str]
    """
    tablero_mod = copy.deepcopy(tablero)

    for i, fila in enumerate(tablero):
        for j, pieza in enumerate(fila):
            if isinstance(pieza, PiezaExplosiva):
                tablero_mod[i][j] = pieza.tipo + str(pieza.alcance)

    return tablero_mod


def encontrar_piezas(tablero: list) -> list:
    """
    Guarda todas las instancias de PiezaExplosiva en un (tablero: list).
    """
    piezas = []
    for fila in tablero:
        for pieza in fila:
            if isinstance(pieza, PiezaExplosiva):
                piezas.append(pieza)

    return piezas


def encontrar_celdas_inalcanzables(tablero: list) -> list:
    """
    Guarda las coordenadas (i, j) de celdas inalcanzables en un (tablero: list).

    Una celda inalcanzable es aquella que no esta dentro del alcance de ninguna pieza explosiva.
    Para esto, utiliza el metodo verificar_alcance_efectivo() de la clase PiezaExplosiva.
    """
    celdas_inalcanzables = []
    piezas = encontrar_piezas(tablero)

    for i, fila in enumerate(tablero):
        for j in range(len(fila)):
            this_cell = []
            for pieza in piezas:
                if pieza.verificar_alcance_efectivo(i, j):
                    this_cell.append((pieza.posicion[0], pieza.posicion[1]))

            if not this_cell:
                celdas_inalcanzables.append((i, j))

    return celdas_inalcanzables


def is_solved(tablero: list, piezas: list) -> str:
    """
    Verifica si el (tablero: list) dado esta resuelto,
    es invalido o es valido pero no esta  resuelto.

    Recibe la lista (piezas: list). Esta contiene las instancias de
    PiezaExplosivas en un tablero para facilitar la verificacion.
    """
    for pieza in piezas:

        i, j = pieza.posicion[0], pieza.posicion[1]

        if funciones.peones_invalidos(tablero) > 0:
            return "invalido"

        if funciones.celdas_afectadas(tablero, i, j) < pieza.alcance:
            return "invalido"

        if funciones.celdas_afectadas(tablero, i, j) > pieza.alcance:
            return "valido pero no resuelto"

    return "resuelto"


def solucionar(
        tablero: list,
        piezas: list,
        inalcanzables: list,
        posicion: tuple = (0, 0)
) -> list | bool:
    """
    Funcion recursiva que recorre un (tablero: list) y lo resuelve.

    Recibe la lista (piezas: list). Esta contiene todas las instancias de PiezaExploiva,
    utilizada para verificar el estado del tablero mediante la funcion is_solved().

    Recibe la lista (inalcanzables: list). Esta contiene las coorenadas (i, j) de las de celdas
    inalcanzables, utilizada para ignorar estas posiciones al recorrer el tablero.

    Recibe la (posicion: tuple) a modificar, necesaria para poder recorrer el tablero
    recursivamente.
    """
    # Verificar el estado del tablero (resuelto, invalido o valido pero no resuelto)
    estado = is_solved(tablero, piezas)

    match estado:
        case "invalido":
            return False
        case "valido pero no resuelto":
            pass
        case "resuelto":
            return True

    # Extraer la posicion actual
    i, j = posicion

    # Recorrer el tablero
    if i < len(tablero):
        j_next = j + 1 if j < len(tablero[0]) - 1 else 0
        i_next = i + 1 if j_next == 0 else i

        # Avanzar a la siguiente posicion sin cambios si:
        # 1. La posicion actual NO esta vacia ("--")
        # 2. La posicion actual es inalcanzable por todas las piezas explosivas
        if tablero[i][j] != "--" or (i, j) in inalcanzables:
            return solucionar(tablero, piezas, inalcanzables, (i_next, j_next))

        # Agregar un peon a la posicion actual
        tablero[i][j] = "PP"

        # Revisar el estado del tablero al agregar el peon
        resultado = solucionar(
            tablero, piezas, inalcanzables, (i_next, j_next))

        # Si agregar el peon no resuelve ni invalida el tablero, solucionar(*args) -> pass,
        # por lo que se mantiene el peon y continua la recursion

        # Si agregar el peon resuelve el tablero, solucionar(*args) -> True,
        # por lo que se retorna el tablero y finaliza la recursion
        if resultado:
            return tablero

        # Si agregar el peon invalida el tablero, solucionar (*args) -> False,
        # por lo que se elimina el peon y continua la recursion
        tablero[i][j] = "--"
        return solucionar(tablero, piezas, inalcanzables, (i_next, j_next))

    return []
