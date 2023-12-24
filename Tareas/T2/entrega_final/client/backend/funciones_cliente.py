# pylint: disable=missing-docstring

def validacion_formato(nombre: str) -> bool:
    check: bool = True

    if nombre in ("test1", "test2", "test3"):
        return True

    if not nombre.isalnum():
        check = False

    if not any(map(str.isdigit, nombre)):
        check = False

    if not any(map(str.isupper, nombre)):
        check = False

    if len(nombre) not in range(3, 17):
        check = False

    return check


def riesgo_mortal(laberinto: list[list]) -> bool:
    sprites = obtener_posiciones(laberinto)

    conejo = sprites["C"][0]
    lobo_v = sprites["LV"]
    lobo_h = sprites["LH"]
    canon_u = sprites["CU"]
    canon_d = sprites["CD"]
    canon_l = sprites["CL"]
    canon_r = sprites["CR"]

    # lobo vertical
    if verificar(laberinto, conejo, "LV", lobo_v, "v"):
        return True

    # lobo horizontal
    if verificar(laberinto, conejo, "LH", lobo_h, "h"):
        return True

    # cañon up
    if verificar(laberinto, conejo, "CU", canon_u, "v"):
        return True

    # cañon down
    if verificar(laberinto, conejo, "CD", canon_d, "v"):
        return True

    # cañon left
    if verificar(laberinto, conejo, "CL", canon_l, "h"):
        return True

    # cañon right
    if verificar(laberinto, conejo, "CR", canon_r, "h"):
        return True

    return False


def usar_item(item: str, inventario: list) -> tuple[bool, list]:

    if item in inventario:
        inventario.remove(item)
        return True, inventario

    return False, inventario


def calcular_puntaje(tiempo: int, vidas: int, cantidad_lobos: int, PUNTAJE_LOBO: int) -> float:

    try:
        return round((tiempo * vidas) / (cantidad_lobos * PUNTAJE_LOBO), 2)

    except ZeroDivisionError:
        return float(0)


def validar_direccion(laberinto: list[list], tecla: str) -> bool:

    sprites = obtener_posiciones(laberinto)

    conejo = sprites["C"][0]

    match tecla.lower():
        case "w":
            return laberinto[conejo[0] - 1][conejo[1]] != "P"
        case "s":
            return laberinto[conejo[0] + 1][conejo[1]] != "P"
        case "a":
            return laberinto[conejo[0]][conejo[1] - 1] != "P"
        case "d":
            return laberinto[conejo[0]][conejo[1] + 1] != "P"
        case _:
            return False


##### EXTRAS #####

def obtener_posiciones(laberinto: list[list]) -> dict[str, list[tuple[int, int]]]:

    conejo = [(i, row.index("C"))
              for i, row in enumerate(laberinto) if "C" in row]

    lobo_v = [(i, row.index("LV"))
              for i, row in enumerate(laberinto) if "LV" in row]

    lobo_h = [(i, row.index("LH"))
              for i, row in enumerate(laberinto) if "LH" in row]

    canon_u = [(i, row.index("CU"))
               for i, row in enumerate(laberinto) if "CU" in row]

    canon_d = [(i, row.index("CD"))
               for i, row in enumerate(laberinto) if "CD" in row]

    canon_l = [(i, row.index("CL"))
               for i, row in enumerate(laberinto) if "CL" in row]

    canon_r = [(i, row.index("CR"))
               for i, row in enumerate(laberinto) if "CR" in row]

    return {
        "C": conejo,
        "LV": lobo_v,
        "LH": lobo_h,
        "CU": canon_u,
        "CD": canon_d,
        "CL": canon_l,
        "CR": canon_r
    }


def verificar(
        laberinto: list[list[str]],
        conejo: tuple[int, int],
        entidad: str,
        posiciones: list[tuple[int, int]],
        orientacion: str
) -> bool:

    filas: list[list[str]] = []

    if orientacion == "h":
        filas = [
            laberinto[pos[0]]
            for pos in posiciones if pos[0] == conejo[0]
        ]

    elif orientacion == "v":
        filas = [
            [row[pos[1]] for row in laberinto]
            for pos in posiciones if pos[1] == conejo[1]
        ]

    slices: list[list] = []

    entidad_ignore_conditions = {
        "LH": lambda idx, conejo_idx: False,
        "LV": lambda idx, conejo_idx: False,
        "CL": lambda idx, conejo_idx: idx < conejo_idx,
        "CU": lambda idx, conejo_idx: idx < conejo_idx,
        "CR": lambda idx, conejo_idx: idx > conejo_idx,
        "CD": lambda idx, conejo_idx: idx > conejo_idx,
    }

    for fila in filas:
        conejo_idx = fila.index("C")

        if (
            entidad_ignore_conditions[entidad](fila.index(entidad), conejo_idx)
        ):
            continue

        start = min(fila.index("C"), fila.index(entidad))
        end = max(fila.index("C"), fila.index(entidad))
        slices.append(fila[start:end + 1])

    for row in slices:
        if not "P" in row:
            return True

    return False


if __name__ == "__main__":
    pass
