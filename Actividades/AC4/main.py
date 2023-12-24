import pickle
from typing import List

from clases import Tortuga


###################
#### ENCRIPTAR ####
###################
def serializar_tortuga(tortuga: Tortuga) -> bytearray:

    try:
        return bytearray(pickle.dumps(tortuga))
    except AttributeError as exc:
        raise ValueError from exc


def verificar_rango(mensaje: bytearray, inicio: int, fin: int) -> None:

    if inicio < 0 or fin > len(mensaje):
        raise AttributeError("El rango es inválido")
    if inicio > fin:
        raise AttributeError("El rango es inválido")
    return None


def codificar_rango(inicio: int, fin: int) -> bytearray:

    return bytearray(inicio.to_bytes(3, "big") + fin.to_bytes(3, "big"))


def codificar_largo(largo: int) -> bytearray:

    return bytearray(largo.to_bytes(3, "big"))


def separar_msg(mensaje: bytearray, inicio: int, fin: int) -> List[bytearray]:

    m_extraido = mensaje[inicio: fin + 1]

    if len(m_extraido) % 2 == 1:
        m_extraido = m_extraido[::-1]

    m_con_mascara = mensaje.copy()
    for value, index in enumerate(range(inicio, fin + 1)):
        m_con_mascara[index] = value

    return [m_extraido, m_con_mascara]


def encriptar(mensaje: bytearray, inicio: int, fin: int) -> bytearray:
    # Se la damos listas
    verificar_rango(mensaje, inicio, fin)

    m_extraido, m_con_mascara = separar_msg(mensaje, inicio, fin)
    rango_codificado = codificar_rango(inicio, fin)
    return (
        codificar_largo(fin - inicio + 1)
        + m_extraido
        + m_con_mascara
        + rango_codificado
    )


######################
#### DESENCRIPTAR ####
######################
def deserializar_tortuga(mensaje_codificado: bytearray) -> Tortuga:

    try:
        return pickle.loads(mensaje_codificado)
    except ValueError as exc:
        raise AttributeError from exc


def decodificar_largo(mensaje: bytearray) -> int:

    return int.from_bytes(mensaje[0:2 + 1], "big")


def separar_msg_encriptado(mensaje: bytearray) -> List[bytearray]:

    m_extraido = mensaje[3:decodificar_largo(mensaje) + 3]

    if len(m_extraido) % 2 == 1:
        m_extraido = m_extraido[::-1]

    m_con_mascara = mensaje[decodificar_largo(mensaje) + 3: -6]

    rango_codificado = mensaje[-6:]

    return [m_extraido, m_con_mascara, rango_codificado]


def decodificar_rango(rango_codificado: bytearray) -> List[int]:

    inicio = int.from_bytes(rango_codificado[:3], "big")
    fin = int.from_bytes(rango_codificado[3:], "big")

    return [inicio, fin]


def desencriptar(mensaje: bytearray) -> bytearray:

    m_extraido, m_con_mascara, rango_codificado = separar_msg_encriptado(
        mensaje)
    inicio, fin = decodificar_rango(rango_codificado)

    for index in range(inicio, fin + 1):
        m_con_mascara[index] = m_extraido[index - inicio]

    return m_con_mascara


if __name__ == "__main__":
    # Tortuga
    tama = Tortuga("Tama2")
    print("Nombre: ", tama.nombre)
    print("Edad: ", tama.edad)
    print(tama.celebrar_anivesario())
    print()

    # Encriptar
    original = serializar_tortuga(tama)
    print("Original: ", original)
    encriptado = encriptar(original, 6, 24)
    print("Encriptado: ", encriptado)
    print()

    # Desencriptar
    mensaje = bytearray(b'\x00\x00\x13roT\x07\x8c\x94sesalc\x06\x8c\x00\x00\x00\x00\x00\x80\x04\x958\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12tuga\x94\x93\x94)\x81\x94}\x94(\x8c\x06nombre\x94\x8c\x05Tama2\x94\x8c\x04edad\x94K\x01ub.\x00\x00\x06\x00\x00\x18')
    desencriptado = desencriptar(mensaje)
    tama = deserializar_tortuga(desencriptado)

    # Tortuga
    print("Tortuga: ", tama)
    print("Nombre: ", tama.nombre)
    print("Edad: ", tama.edad)
