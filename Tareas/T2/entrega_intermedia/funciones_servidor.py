# pylint: disable=missing-docstring

from itertools import cycle


def usuario_permitido(nombre: str, usuarios_no_permitidos: list[str]) -> bool:

    if nombre in usuarios_no_permitidos:
        return False

    return True


def serializar_mensaje(mensaje: str) -> bytearray:

    return bytearray(mensaje.encode(encoding="utf-8"))


def separar_mensaje(mensaje: bytearray) -> list[bytearray]:

    empty = [[] for _ in range(3)]

    for i, j in zip(mensaje, cycle([0, 1, 2, 2, 1, 0])):
        empty[j].append(i)

    return [bytearray(i) for i in empty]


def encriptar_mensaje(mensaje: bytearray) -> bytearray:

    A, B, C = separar_mensaje(mensaje)  # pylint: disable=invalid-name

    mod = A[0] + B[-1] + C[0]

    if mod % 2 == 0:
        return bytearray(b"1") + A + C + B

    return bytearray(b"0") + B + A + C


def codificar_mensaje(mensaje: bytearray) -> list[bytearray]:

    length = len(mensaje)

    blocks = length // 36

    padding = 36 - (length % 36)

    padded_msg = mensaje

    if not length % 36 == 0:
        blocks += 1
        padded_msg += bytearray(b"\x00" * padding)

    final_msg = [bytearray(length.to_bytes(4, byteorder="big"))]

    for i in range(blocks):
        final_msg.append(bytearray((i + 1).to_bytes(4, byteorder="big")))
        final_msg.append(bytearray(padded_msg[36 * i:36 * (i + 1)]))

    return final_msg


if __name__ == "__main__":
    pass
