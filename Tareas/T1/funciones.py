"""
Metodos de tablero.py transferidos a una funcion para poder ser reutilizados.
"""

from pieza_explosiva import PiezaExplosiva


def peones_invalidos(tablero: list) -> int:
    """
    Cuenta la cantidad de peones invalidos (2+ peones adyacentes) en un (tablero: list)
    """
    n_filas, n_columnas = len(tablero), len(tablero[0])
    invalidos = 0
    peones = []

    # Buscar y guardar coordenadas (i, j) de todos los peones
    for fila in range(n_filas):
        for columna in range(n_columnas):
            if tablero[fila][columna] == "PP":
                peones.append((fila, columna))

    # Contar cantidad de vecinos
    for peon in peones:
        vecinos = 0

        # Revisar todas las posiciones posibles para un vecino del peon
        for coordenada in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            posible_posicion = tuple(map(sum, zip(peon, coordenada)))

            if posible_posicion in peones:
                vecinos += 1

        if vecinos > 1:
            invalidos += 1

    return invalidos


def celdas_afectadas(tablero: list, fila: int, columna: int) -> int:
    """
    Cuenta la cantidad de celdas afectadas por una pieza explosiva en la
    posicion (fila: int, columna: int) en un (tablero: list) dado.
    """
    celdas = 1
    pieza = tablero[fila][columna]
    dimensiones = [len(tablero), len(tablero[0])]

    # Verificar que la pieza sea una instancia de PiezaExplosiva
    if not isinstance(pieza, PiezaExplosiva):
        return -1

    # Contar celdas afectadas en 8 posibles direcciones
    def revision_izquierda() -> int:
        n_celdas = 0
        for i in range(columna - 1, -1, -1):
            if tablero[fila][i] != "PP":
                n_celdas += 1
            else:
                break
        return n_celdas

    def revision_derecha() -> int:
        n_celdas = 0
        for i in range(columna + 1, dimensiones[1]):
            if tablero[fila][i] != "PP":
                n_celdas += 1
            else:
                break
        return n_celdas

    def revision_arriba() -> int:
        n_celdas = 0
        for i in range(fila - 1, -1, -1):
            if tablero[i][columna] != "PP":
                n_celdas += 1
            else:
                break
        return n_celdas

    def revision_abajo() -> int:
        n_celdas = 0
        for i in range(fila + 1, dimensiones[0]):
            if tablero[i][columna] != "PP":
                n_celdas += 1
            else:
                break
        return n_celdas

    def revision_diagonal_izquierda_arriba() -> int:
        n_celdas = 0
        for i in range(1, min(fila, columna) + 1):
            if tablero[fila - i][columna - i] != "PP":
                n_celdas += 1
            else:
                break
        return n_celdas

    def revision_diagonal_derecha_arriba() -> int:
        n_celdas = 0
        for i in range(1, min(fila + 1, dimensiones[1] - columna)):
            if tablero[fila - i][columna + i] != "PP":
                n_celdas += 1
            else:
                break
        return n_celdas

    def revision_diagonal_izquierda_abajo() -> int:
        n_celdas = 0
        for i in range(1, min(dimensiones[0] - fila, columna + 1)):
            if tablero[fila + i][columna - i] != "PP":
                n_celdas += 1
            else:
                break
        return n_celdas

    def revision_diagonal_derecha_abajo() -> int:
        n_celdas = 0
        for i in range(1, min(dimensiones[0] - fila, dimensiones[1] - columna)):
            if tablero[fila + i][columna + i] != "PP":
                n_celdas += 1
            else:
                break
        return n_celdas

    # Sumar segun el tipo de pieza
    match pieza.tipo:
        case "H":
            celdas += (revision_izquierda() +
                       revision_derecha())

        case "V":
            celdas += (revision_arriba() +
                       revision_abajo())

        case "R":
            celdas += (revision_izquierda() +
                       revision_derecha() +
                       revision_arriba() +
                       revision_abajo() +
                       revision_diagonal_izquierda_arriba() +
                       revision_diagonal_derecha_arriba() +
                       revision_diagonal_izquierda_abajo() +
                       revision_diagonal_derecha_abajo())

    return celdas
