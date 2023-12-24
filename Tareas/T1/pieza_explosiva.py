class PiezaExplosiva:
    def __init__(self, alcance: int, tipo: str, posicion: list) -> None:
        self.alcance = alcance
        self.tipo = tipo
        self.posicion = posicion

    def __str__(self) -> str:
        fila, columna = self.posicion
        texto = f"Soy la pieza {self.tipo}{self.alcance}\n"
        texto += f"\tEstoy en la fila {fila} y columna {columna}\n"
        return texto

    def verificar_alcance(self, fila: int, columna: int) -> bool:
        match self.tipo:
            case "H":
                return verificar_h(self.posicion, fila)
            case "V":
                return verificar_v(self.posicion, columna)
            case "R":
                return verificar_r(self.posicion, fila, columna)
            case _:
                return False

    # EXTRA #
    def verificar_alcance_efectivo(self, fila: int, columna: int) -> bool:
        """
        Verifica si una celda con coordenadas (fila: int, columna: int)
        es alcanzable por una pieza.

        Este metodo considera el alcance maximo de la pieza.
        """
        match self.tipo:
            case "H":
                return verificar_h_efectivo(self.posicion, fila, columna, self.alcance)
            case "V":
                return verificar_v_efectivo(self.posicion, fila, columna, self.alcance)
            case "R":
                return verificar_r_efectivo(self.posicion, fila, columna, self.alcance)
            case _:
                return False
    # EXTRA #


def verificar_h(posicion: list, i: int) -> bool:
    if posicion[0] == i:
        return True

    return False


def verificar_v(posicion: list, j: int) -> bool:
    if posicion[1] == j:
        return True

    return False


def verificar_r(posicion: list, i: int, j: int) -> bool:
    if verificar_h(posicion, i):
        return True

    if verificar_v(posicion, j):
        return True

    if abs(posicion[0] - i) == abs(posicion[1] - j):
        return True

    return False


# EXTRA #
def verificar_h_efectivo(posicion: list, i: int, j: int, alcance: int) -> bool:
    """
    Verifica si una celda con coordenadas (i: int, j: int)
    es alcanzable por una pieza de tipo H.

    Esta funcion considera el alcance maximo de la pieza.
    """
    if posicion[0] == i and abs(posicion[1] - j) <= alcance:
        return True

    return False


def verificar_v_efectivo(posicion: list, i: int, j: int, alcance: int) -> bool:
    """
    Verifica si una celda con coordenadas (i: int, j: int)
    es alcanzable por una pieza de tipo V.

    Esta funcion considera el alcance maximo de la pieza.
    """
    if posicion[1] == j and abs(posicion[0] - i) <= alcance:
        return True

    return False


def verificar_r_efectivo(posicion: list, i: int, j: int, alcance: int) -> bool:
    """
    Verifica si una celda con coordenadas (i: int, j: int)
    es alcanzable por una pieza de tipo R.

    Esta funcion considera el alcance maximo de la pieza.
    """
    if verificar_h_efectivo(posicion, i, j, alcance):
        return True

    if verificar_v_efectivo(posicion, i, j, alcance):
        return True

    if abs(posicion[0] - i) == abs(posicion[1] - j) and abs(posicion[0] - i) <= alcance:
        return True

    return False
# EXTRA #
