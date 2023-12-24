class Item:
    def __init__(self, nombre: str, precio: int, puntos: int):
        self.nombre = nombre
        self._precio = precio
        self.puntos = puntos

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, value):
        print(f"Nice try bozo... {value}? fr?")


class Usuario:
    def __init__(self, suscripcion: bool, canasta: list, puntos: int):
        self.sub = suscripcion
        self.canasta = canasta
        self._puntos = puntos

    def agregar_item(self, item: Item):
        ...

    @property
    def puntos(self):
        return self._puntos

    @puntos.setter
    def puntos(self, value):
        print(f"Nice try bozo... {value}? fr?")
