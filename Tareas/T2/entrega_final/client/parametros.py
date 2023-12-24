"""General parameters of the game."""

# pylint: disable=E0611

import os

from PyQt6.QtCore import Qt

# No modificar

ANCHO_LABERINTO = 16
LARGO_LABERINTO = 16

# Corresponde a la duración en el primer laberinto, en segundos
DURACION_NIVEL_INICIAL = 120
VELOCIDAD_LOBO = 5  # Corresponde a la velocidad en el primer laberinto
PONDERADOR_LABERINTO_1 = 1
PONDERADOR_LABERINTO_2 = 0.9
PONDERADOR_LABERINTO_3 = 0.8
PUNTAJE_LOBO = 3
CANTIDAD_VIDAS = 3
VELOCIDAD_CONEJO = 10
VELOCIDAD_ZANAHORIA = 8

TIEMPO_BOMBA = 5
PUNTAJE_INF = 350

# Agregue los parámetros necesarios


# VALUES

CELL_SIZE = 40

DIRECTIONS = {
    Qt.Key.Key_W.value: "UP",
    Qt.Key.Key_S.value: "DOWN",
    Qt.Key.Key_A.value: "LEFT",
    Qt.Key.Key_D.value: "RIGHT",
}

MODIFIED_LEVEL_TIME = {
    1: int(DURACION_NIVEL_INICIAL * PONDERADOR_LABERINTO_1),
    2: int(DURACION_NIVEL_INICIAL * PONDERADOR_LABERINTO_2),
    3: int(DURACION_NIVEL_INICIAL * PONDERADOR_LABERINTO_2 * PONDERADOR_LABERINTO_3),
}

MODIFIED_WOLF_SPEED = {
    1: int(1000 / (VELOCIDAD_LOBO / PONDERADOR_LABERINTO_1)),
    2: int(1000 / (VELOCIDAD_LOBO / PONDERADOR_LABERINTO_2)),
    3: int(1000 / (VELOCIDAD_LOBO / PONDERADOR_LABERINTO_2 / PONDERADOR_LABERINTO_3)),
}

TRANSLATOR = {
    "WOLF": {
        "LH": "H",
        "LV": "V",
    },

    "CANNON": {
        "CU": "UP",
        "CD": "DOWN",
        "CL": "LEFT",
        "CR": "RIGHT",
    }
}

POSITIONS = {
    "RABBIT": (1, 1),
    "WOLF": {},
    "CARROT": {},
}

# PATHS

MAZES = {
    1: os.path.join("assets", "laberintos", "tablero_1.txt"),
    2: os.path.join("assets", "laberintos", "tablero_2.txt"),
    3: os.path.join("assets", "laberintos", "tablero_3.txt")
}

FLOOR = os.path.join("assets", "sprites", "bloque_fondo.jpeg")
WALL = os.path.join("assets", "sprites", "bloque_pared.jpeg")

RABBIT = {
    "IDLE": {
        0: os.path.join("assets", "sprites", "conejo.png"),
    },

    "UP": {
        0: os.path.join("assets", "sprites", "conejo_arriba_1.png"),
        1: os.path.join("assets", "sprites", "conejo_arriba_2.png"),
        2: os.path.join("assets", "sprites", "conejo_arriba_3.png"),
    },

    "DOWN": {
        0: os.path.join("assets", "sprites", "conejo_abajo_1.png"),
        1: os.path.join("assets", "sprites", "conejo_abajo_2.png"),
        2: os.path.join("assets", "sprites", "conejo_abajo_3.png"),
    },

    "LEFT": {
        0: os.path.join("assets", "sprites", "conejo_izquierda_1.png"),
        1: os.path.join("assets", "sprites", "conejo_izquierda_2.png"),
        2: os.path.join("assets", "sprites", "conejo_izquierda_3.png"),
    },

    "RIGHT": {
        0: os.path.join("assets", "sprites", "conejo_derecha_1.png"),
        1: os.path.join("assets", "sprites", "conejo_derecha_2.png"),
        2: os.path.join("assets", "sprites", "conejo_derecha_3.png"),
    },
}


WOLF = {
    "UP": {
        0: os.path.join("assets", "sprites", "lobo_vertical_arriba_1.png"),
        1: os.path.join("assets", "sprites", "lobo_vertical_arriba_2.png"),
        2: os.path.join("assets", "sprites", "lobo_vertical_arriba_3.png"),
    },

    "DOWN": {
        0: os.path.join("assets", "sprites", "lobo_vertical_abajo_1.png"),
        1: os.path.join("assets", "sprites", "lobo_vertical_abajo_2.png"),
        2: os.path.join("assets", "sprites", "lobo_vertical_abajo_3.png"),
    },

    "LEFT": {
        0: os.path.join("assets", "sprites", "lobo_horizontal_izquierda_1.png"),
        1: os.path.join("assets", "sprites", "lobo_horizontal_izquierda_2.png"),
        2: os.path.join("assets", "sprites", "lobo_horizontal_izquierda_3.png"),
    },

    "RIGHT": {
        0: os.path.join("assets", "sprites", "lobo_horizontal_derecha_1.png"),
        1: os.path.join("assets", "sprites", "lobo_horizontal_derecha_2.png"),
        2: os.path.join("assets", "sprites", "lobo_horizontal_derecha_3.png"),
    },
}

CANNON = {
    "CU": os.path.join("assets", "sprites", "canon_arriba.png"),
    "CD": os.path.join("assets", "sprites", "canon_abajo.png"),
    "CL": os.path.join("assets", "sprites", "canon_izquierda.png"),
    "CR": os.path.join("assets", "sprites", "canon_derecha.png"),
}


CARROT = {
    "UP": os.path.join("assets", "sprites", "zanahoria_arriba.png"),
    "DOWN": os.path.join("assets", "sprites", "zanahoria_abajo.png"),
    "LEFT": os.path.join("assets", "sprites", "zanahoria_izquierda.png"),
    "RIGHT": os.path.join("assets", "sprites", "zanahoria_derecha.png"),
}

APPLE_BOMB = os.path.join("assets", "sprites", "manzana.png")
FREEZE_BOMB = os.path.join("assets", "sprites", "congelacion_burbuja.png")

FIRE_ZONE = os.path.join("assets", "sprites", "explosion.png")
ICE_ZONE = os.path.join("assets", "sprites", "congelacion.png")

HEART = os.path.join("assets_extra", "pink_heart.png")
GOLDEN_HEART = os.path.join("assets_extra", "golden_heart.png")

LOGO = os.path.join("assets", "sprites", "logo.png")

VICTORY = os.path.join("assets", "sonidos", "victoria.wav")
DEFEAT = os.path.join("assets", "sonidos", "derrota.wav")
ERROR = os.path.join("assets_extra", "error.wav")

if __name__ == '__main__':
    pass
