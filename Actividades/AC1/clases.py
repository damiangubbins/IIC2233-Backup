from abc import ABC, abstractmethod


class Vehiculo(ABC):

    identificador = 0

    def __init__(self, rendimiento: int, marca: str, energia: int = 120, *args, **kwargs):
        self.identificador = Vehiculo.identificador
        Vehiculo.identificador += 1

        self.rendimiento = rendimiento
        self.marca = marca
        self._energia = energia

    @abstractmethod
    def recorrer(self, kilometros) -> tuple:
        if self.autonomia >= kilometros:
            recorrido = kilometros
        else:
            recorrido = self.autonomia

        delta_energia = int(recorrido / self.rendimiento)

        self.energia = delta_energia

        return (recorrido, delta_energia)

    @property
    def autonomia(self) -> float:
        return self.energia * self.rendimiento

    @property
    def energia(self) -> int:
        return self._energia

    @energia.setter
    def energia(self, value) -> None:
        self._energia = max(0, self._energia - value)


class AutoBencina(Vehiculo):

    def __init__(self, bencina_favorita: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bencina_favorita = bencina_favorita

    def recorrer(self, kilometros) -> str:

        recorrido, delta_energia = super().recorrer(kilometros)
        return f"Anduve por {recorrido}Km y gasté {delta_energia}L de bencina"


class AutoElectrico(Vehiculo):

    def __init__(self, vida_util_bateria: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vida_util_bateria = vida_util_bateria

    def recorrer(self, kilometros) -> str:

        recorrido, delta_energia = super().recorrer(kilometros)
        return f"Anduve por {recorrido}Km y gasté {delta_energia}W de energía eléctrica"


class Camioneta(AutoBencina):

    def __init__(self, capacidad_maleta: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.capacidad_maleta = capacidad_maleta


class Telsa(AutoElectrico):

    def __init__(self, *args, **kwargs):
        AutoElectrico.__init__(self, *args, **kwargs)

    def recorrer(self, kilometros) -> str:
        return super().recorrer(kilometros) + "de forma inteligente"


class FaitHibrido(AutoBencina, AutoElectrico):

    def __init__(self, *args, **kwargs):
        super().__init__(vida_util_bateria=5, *args, **kwargs)

    def recorrer(self, kilometros: int) -> str:
        return f"{AutoBencina.recorrer(self, kilometros/2)}\
{AutoElectrico.recorrer(self, kilometros/2)}"
