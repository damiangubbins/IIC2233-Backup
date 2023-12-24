from collections import defaultdict
from copy import copy
from functools import reduce
from itertools import product
from typing import Generator

from parametros import RUTA_GENEROS, RUTA_PELICULAS
from utilidades import (Genero, Pelicula, imprimir_generos, imprimir_peliculas,
                        imprimir_peliculas_genero, obtener_unicos)

# ----------------------------------------------------------------------------
# Parte 1: Cargar dataset
# ----------------------------------------------------------------------------


def cargar_peliculas(ruta: str) -> Generator:

    def transform(element):
        if element.isnumeric():
            return int(element)
        if "." in element:
            return float(element)
        return element

    with open(ruta, 'r') as archivo:
        peliculas = archivo.readlines()[1:]
        for pelicula in peliculas:
            datos_pelicula = map(transform, pelicula.strip().split(','))
            pelicula = Pelicula(*datos_pelicula)
            yield pelicula


def cargar_generos(ruta: str) -> Generator:

    def transform(element):
        if element.isnumeric():
            return int(element)
        return element

    with open(ruta, 'r') as archivo:
        generos = archivo.readlines()[1:]
        for genero in generos:
            datos_genero = map(transform, genero.strip().split(','))
            genero = Genero(*datos_genero)
            yield genero


# ----------------------------------------------------------------------------
# Parte 2: Consultas sobre generadores
# ----------------------------------------------------------------------------

def obtener_directores(generador_peliculas: Generator) -> set:

    return obtener_unicos(map(lambda x: x.director, generador_peliculas))


def obtener_str_titulos(generador_peliculas: Generator) -> str:

    try:
        return reduce(lambda x, y: f"{x}, {y}", map(lambda x: x.titulo, generador_peliculas))
    except TypeError:
        return ""


def filtrar_peliculas(
    generador_peliculas: Generator,
    director: str | None = None,
    rating_min: float | None = None,
    rating_max: float | None = None
) -> filter:

    if director is not None:
        generador_peliculas = filter(
            lambda x: x.director == director, generador_peliculas)  # type: ignore
    if rating_min is not None:
        generador_peliculas = filter(
            lambda x: x.rating >= rating_min, generador_peliculas)  # type: ignore
    if rating_max is not None:
        generador_peliculas = filter(
            lambda x: x.rating <= rating_max, generador_peliculas)  # type: ignore

    return filter(None, generador_peliculas)


def filtrar_peliculas_por_genero(
    generador_peliculas: Generator,
    generador_generos: Generator,
    genero: str | None = None
) -> filter:

    if genero is not None:
        generador_generos = filter(
            lambda x: x.genero == genero, generador_generos)  # type: ignore

    return filter(
        lambda x: x[0].id_pelicula == x[1].id_pelicula,
        product(generador_peliculas, generador_generos))


# ----------------------------------------------------------------------------
# Parte 3: Iterables
# ----------------------------------------------------------------------------

class DCCMax:

    def __init__(self, peliculas: list) -> None:
        self.peliculas = peliculas

    def __iter__(self):
        return IteradorDCCMax(self.peliculas)


class IteradorDCCMax:

    def __init__(self, iterable_peliculas: list) -> None:
        self.peliculas = copy(iterable_peliculas)
        self.peliculas.sort(key=lambda x: (x.estreno, x.rating*-1))

    def __iter__(self):
        return self

    def __next__(self) -> tuple:
        if self.peliculas:
            return self.peliculas.pop(0)

        # Se levanta la excepción correspondiente
        raise StopIteration()


if __name__ == '__main__':
    print('> Cargar películas:')
    imprimir_peliculas(cargar_peliculas(RUTA_PELICULAS))
    print()

    print('> Cargar géneros')
    imprimir_generos(cargar_generos(RUTA_GENEROS), 5)
    print()

    print('> Obtener directores:')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    print(list(obtener_directores(generador_peliculas)))
    print()

    print('> Obtener string títulos')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    print(obtener_str_titulos(generador_peliculas))
    print()

    print('> Filtrar películas (por director):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(
        generador_peliculas, director='Christopher Nolan'
    ))
    print('\n> Filtrar películas (rating min):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(generador_peliculas, rating_min=9.1))
    print('\n> Filtrar películas (rating max):')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    imprimir_peliculas(filtrar_peliculas(generador_peliculas, rating_max=8.7))
    print()

    print('> Filtrar películas por género')
    generador_peliculas = cargar_peliculas(RUTA_PELICULAS)
    generador_generos = cargar_generos(RUTA_GENEROS)
    imprimir_peliculas_genero(filtrar_peliculas_por_genero(
        generador_peliculas, generador_generos, 'Biography'
    ))
    print()

    print('> DCC Max')
    for (estreno, pelis) in DCCMax(list(cargar_peliculas(RUTA_PELICULAS))):
        print(f'\n{estreno:^80}\n')
        imprimir_peliculas(pelis)
