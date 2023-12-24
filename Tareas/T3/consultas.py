import collections
import datetime
import functools
import itertools
import math
from typing import Generator

import utilidades


def peliculas_genero(generador_peliculas: Generator, genero: str):
    return filter(lambda pelicula: pelicula.genero == genero, generador_peliculas)


def personas_mayores(generador_personas: Generator, edad: int):
    return filter(lambda persona: persona.edad >= edad, generador_personas)


def funciones_fecha(generador_funciones: Generator, fecha: str):
    fecha = fecha.replace(fecha[5:8], "-")
    return filter(lambda funcion: funcion.fecha == fecha, generador_funciones)


def titulo_mas_largo(generador_peliculas: Generator) -> str:
    peliculas = [pelicula for pelicula in generador_peliculas]
    peliculas.sort(key=lambda pelicula: pelicula.rating)
    peliculas.sort(key=lambda pelicula: len(pelicula.titulo))

    return peliculas[-1].titulo


def normalizar_fechas(generador_funciones: Generator):
    def two_to_four(funcion: utilidades.Funciones):
        fecha = funcion.fecha

        day = fecha[0:2]
        month = fecha[3:5]
        year = (
            "20" + fecha[6:8] if int(fecha[6:8]) in range(0,
                                                          24) else "19" + fecha[6:8]
        )

        fecha = year + "-" + month + "-" + day

        return utilidades.Funciones(
            funcion.id, funcion.numero_sala, funcion.id_pelicula, funcion.horario, fecha
        )

    return map(two_to_four, generador_funciones)


def personas_reservas(generador_reservas: Generator):
    return {reserva.id_persona for reserva in generador_reservas}


def peliculas_en_base_al_rating(
    generador_peliculas: Generator, genero: str, rating_min: int, rating_max: int
):
    return filter(
        lambda pelicula: pelicula.genero == genero
        and rating_min <= pelicula.rating <= rating_max,
        generador_peliculas,
    )


def mejores_peliculas(generador_peliculas: Generator):
    peliculas = [pelicula for pelicula in generador_peliculas]

    peliculas.sort(key=lambda pelicula: pelicula.id)
    peliculas.sort(key=lambda pelicula: pelicula.rating, reverse=True)

    return peliculas[:20]


def pelicula_genero_mayor_rating(generador_peliculas: Generator, genero: str) -> str:
    try:
        return max(
            peliculas_genero(generador_peliculas, genero),
            key=lambda pelicula: pelicula.rating,
        ).titulo
    except ValueError:
        return ""


def fechas_funciones_pelicula(
    generador_peliculas: Generator, generador_funciones: Generator, titulo: str
):
    ids = [pelicula.id for pelicula in generador_peliculas if pelicula.titulo == titulo]
    return [
        funcion.fecha for funcion in generador_funciones if funcion.id_pelicula in ids
    ]


def genero_mas_transmitido(
    generador_peliculas: Generator, generador_funciones: Generator, fecha: str
) -> str:
    # //! fecha "dd-mm-yyyy"
    # //! funcion.fecha "dd-mm-yy"

    fecha = fecha.replace(fecha[5:8], "-")

    ids = [
        funcion.id_pelicula for funcion in generador_funciones if funcion.fecha == fecha
    ]

    if not ids:
        return ""

    generos = [
        pelicula.genero for pelicula in generador_peliculas if pelicula.id in ids
    ]
    return max(generos, key=generos.count)


def id_funciones_genero(
    generador_peliculas: Generator, generador_funciones: Generator, genero: str
):
    id_peliculas = [
        pelicula.id for pelicula in generador_peliculas if pelicula.genero == genero
    ]
    return [
        funcion.id
        for funcion in generador_funciones
        if funcion.id_pelicula in id_peliculas
    ]


def butacas_por_funcion(
    generador_reservas: Generator, generador_funciones: Generator, id_funcion: int
) -> int:
    id_funciones = [funcion.id for funcion in generador_funciones]
    if id_funcion not in id_funciones:
        return 0
    return len(
        [reserva for reserva in generador_reservas if reserva.id_funcion == id_funcion]
    )


def salas_de_pelicula(
    generador_peliculas: Generator, generador_funciones: Generator, nombre_pelicula: str
):
    id_peliculas = [
        pelicula.id
        for pelicula in generador_peliculas
        if pelicula.titulo == nombre_pelicula
    ]
    return [
        funcion.numero_sala
        for funcion in generador_funciones
        if funcion.id_pelicula in id_peliculas
    ]


def nombres_butacas_altas(
    generador_personas: Generator,
    generador_peliculas: Generator,
    generador_reservas: Generator,
    generador_funciones: Generator,
    titulo: str,
    horario: int,
):
    id_peliculas = [
        pelicula.id for pelicula in generador_peliculas if pelicula.titulo == titulo
    ]
    id_funciones = [
        funcion.id
        for funcion in generador_funciones
        if funcion.id_pelicula in id_peliculas and funcion.horario == horario
    ]
    id_personas = [
        reserva.id_persona
        for reserva in generador_reservas
        if reserva.id_funcion in id_funciones
    ]
    return [
        persona.nombre for persona in generador_personas if persona.id in id_personas
    ]


def nombres_persona_genero_mayores(
    generador_personas: Generator,
    generador_peliculas: Generator,
    generador_reservas: Generator,
    generador_funciones: Generator,
    nombre_pelicula: str,
    genero: str,
    edad: int,
):
    id_peliculas = [
        peicula.id
        for peicula in generador_peliculas
        if peicula.titulo == nombre_pelicula
    ]
    id_funciones = [
        funcion.id
        for funcion in generador_funciones
        if funcion.id_pelicula in id_peliculas
    ]
    id_reservas = [
        reserva.id_persona
        for reserva in generador_reservas
        if reserva.id_funcion in id_funciones
    ]
    return {
        persona.nombre
        for persona in generador_personas
        if persona.id in id_reservas
        and persona.genero == genero
        and persona.edad >= edad
    }


def genero_comun(
    generador_personas: Generator,
    generador_peliculas: Generator,
    generador_reservas: Generator,
    generador_funciones: Generator,
    id_funcion: int,
) -> str:
    funcion = [funcion for funcion in generador_funciones if funcion.id == id_funcion][
        0
    ]

    nombre_pelicula = [
        pelicula.titulo
        for pelicula in generador_peliculas
        if pelicula.id == funcion.id_pelicula
    ][0]

    id_reservas = [
        reserva.id_persona
        for reserva in generador_reservas
        if reserva.id_funcion == id_funcion
    ]
    generos = [
        persona.genero for persona in generador_personas if persona.id in id_reservas
    ]
    count_generos = collections.Counter(generos)

    generos = [
        genero
        for genero in count_generos
        if count_generos[genero] == max(count_generos.values())
    ]

    if len(generos) == 1:
        return f"En la función {id_funcion} de la película {nombre_pelicula} \
la mayor parte del público es {generos[0]}."

    if len(generos) == 2:
        return f"En la función {id_funcion} de la película {nombre_pelicula} \
se obtiene que la mayor parte del público es de {generos[0]} y {generos[1]} \
con la misma cantidad de personas."

    return f"En la función {id_funcion} de la película {nombre_pelicula} \
se obtiene que la cantidad de personas es igual para todos los géneros."


def edad_promedio(
    generador_personas: Generator,
    generador_peliculas: Generator,
    generador_reservas: Generator,
    generador_funciones: Generator,
    id_funcion: int,
) -> str:
    funcion = [funcion for funcion in generador_funciones if funcion.id == id_funcion][
        0
    ]

    nombre_pelicula = [
        pelicula.titulo
        for pelicula in generador_peliculas
        if pelicula.id == funcion.id_pelicula
    ][0]

    id_reservas = [
        reserva.id_persona
        for reserva in generador_reservas
        if reserva.id_funcion == id_funcion
    ]
    edades = [
        persona.edad for persona in generador_personas if persona.id in id_reservas
    ]
    return f"En la función {id_funcion} de la película {nombre_pelicula} \
la edad promedio del público es {math.ceil(sum(edades) / len(edades))}."


def obtener_horarios_disponibles(
    generador_peliculas: Generator,
    generador_reservas: Generator,
    generador_funciones: Generator,
    fecha_funcion: str,
    reservas_maximas: int,
):
    funciones = [
        funcion for funcion in generador_funciones if funcion.fecha == fecha_funcion
    ]

    reservas = [
        reserva.id_funcion
        for reserva in generador_reservas
        if reserva.id_funcion in [funcion.id for funcion in funciones]
    ]

    if not reservas:
        return reservas

    count_reservas = {funcion.id: reservas.count(
        funcion.id) for funcion in funciones}

    reservas_validas = [
        _id for _id in count_reservas if count_reservas[_id] < reservas_maximas
    ]

    if not reservas_validas:
        return reservas_validas

    funciones_validas = [
        funcion for funcion in funciones if funcion.id in reservas_validas
    ]

    if not funciones_validas:
        return funciones_validas

    peliculas = [
        pelicula
        for pelicula in generador_peliculas
        if pelicula.id in [funcion.id_pelicula for funcion in funciones_validas]
    ]

    if not peliculas:
        return peliculas

    peliculas.sort(key=lambda pelicula: pelicula.rating)
    pelicula = peliculas[-1]

    horarios = {
        funcion.horario
        for funcion in funciones_validas
        if funcion.id_pelicula == pelicula.id
    }

    return horarios


def personas_no_asisten(
    generador_personas: Generator,
    generador_reservas: Generator,
    generador_funciones: Generator,
    fecha_inicio: str,
    fecha_termino: str,
):
    fecha_i_date = datetime.datetime.strptime(fecha_inicio, "%d-%m-%Y").date()
    fecha_t_date = datetime.datetime.strptime(fecha_termino, "%d-%m-%Y").date()

    ids_funciones = [
        funcion.id
        for funcion in generador_funciones
        if fecha_i_date
        <= datetime.datetime.strptime(funcion.fecha, "%d-%m-%y").date()
        <= fecha_t_date
    ]

    ids_personas_reserva = [
        reserva.id_persona
        for reserva in generador_reservas
        if reserva.id_funcion in ids_funciones
    ]

    personas_validas = [
        persona
        for persona in generador_personas
        if persona.id not in ids_personas_reserva
    ]
    return personas_validas
