import copy

import extras
import funciones
from imprimir_tablero import imprimir_tablero
from pieza_explosiva import PiezaExplosiva


class Tablero:
    def __init__(self, tablero: list) -> None:
        # filas         #columnas
        self.dimensiones = [len(tablero), len(tablero[0])]
        self.tablero = tablero

    @property
    def desglose(self) -> list:

        valores = [0, 0, 0]
        piezas = ("H", "V", "R")
        n_filas, n_columnas = self.dimensiones

        for i in range(n_filas):
            for j in range(n_columnas):
                if self.tablero[i][j][0] in piezas:
                    valores[0] += 1
                elif "P" in self.tablero[i][j]:
                    valores[1] += 1
                else:
                    valores[2] += 1

        return valores

    @property
    def peones_invalidos(self) -> int:
        return funciones.peones_invalidos(self.tablero)

    @property
    def piezas_explosivas_invalidas(self) -> int:

        n_filas, n_columnas = self.dimensiones
        invalidos = 0
        piezas = extras.encontrar_piezas(self.tablero_transformado)

        for pieza in piezas:
            alcance_total = 0
            for i in range(n_filas):
                for j in range(n_columnas):
                    if pieza.verificar_alcance(i, j):
                        alcance_total += 1

            if alcance_total < pieza.alcance:
                invalidos += 1

        return invalidos

    @property
    def tablero_transformado(self) -> list:

        piezas = ("H", "V", "R")
        tablero_mod = copy.deepcopy(self.tablero)

        for i, fila in enumerate(self.tablero):
            for j, columna in enumerate(fila):
                if columna[0] in piezas:
                    tablero_mod[i][j] = PiezaExplosiva(
                        int(columna[1:]), columna[0], [i, j])

        return tablero_mod

    def celdas_afectadas(self, fila: int, columna: int) -> int:
        return funciones.celdas_afectadas(self.tablero_transformado, fila, columna)

    def limpiar(self) -> None:
        for i, fila in enumerate(self.tablero):
            for j, pieza in enumerate(fila):
                if pieza == "PP":
                    self.tablero[i][j] = "--"

    def reemplazar(self, nombre_nuevo_tablero: str) -> bool:
        tableros = extras.leer_tableros_txt()

        if nombre_nuevo_tablero not in tableros.keys():
            return False

        self.tablero = extras.txt_a_list(nombre_nuevo_tablero)
        self.dimensiones = [len(self.tablero), len(self.tablero[0])]

        return True

    def solucionar(self) -> list:

        # Verificar validez del tablero
        if self.piezas_explosivas_invalidas:
            print(extras.print_consola(
                f"{self.piezas_explosivas_invalidas} pieza(s) invalida(s)"))
            return []

        if self.peones_invalidos:
            print(extras.print_consola(
                f"{self.peones_invalidos} peon(es) invalido(s)"))
            return []

        if not self.desglose[0]:
            print(extras.print_consola("Tablero vacío"))
            return self.tablero

        # Preparar el tablero para solucionar
        tablero_a_solucionar = copy.deepcopy(self.tablero_transformado)
        piezas = extras.encontrar_piezas(self.tablero_transformado)
        inalcanzables = extras.encontrar_celdas_inalcanzables(
            self.tablero_transformado)

        # Verificar si el tablero ya esta resuelto
        if extras.is_solved(self.tablero_transformado, piezas) == "resuelto":
            print(extras.print_consola("Tablero resuelto"))
            return self.tablero

        # Solucionar el tablero
        solucion = extras.solucionar(
            tablero=tablero_a_solucionar,
            piezas=piezas,
            inalcanzables=inalcanzables
        )

        # Mostrar resultado
        if not solucion:
            print(extras.print_consola("Tablero sin solución"))
            return []

        solucion = extras.tranformar_inversa(solucion)

        imprimir_tablero(solucion)

        return solucion
