# pylint: disable=missing-docstring, W3101

import requests

import api


class Peliculas:
    def __init__(self, host, port):
        self.base = f"http://{host}:{port}"

    def saludar(self) -> dict:
        req = requests.get(self.base)
        exit_code = req.status_code
        response = req.json()

        return {"status-code": exit_code, "saludo": response["result"]}

    def verificar_informacion(self, pelicula: str) -> bool:
        req = requests.get(f"{self.base}/peliculas")
        exit_code = req.status_code
        response = req.json()

        return pelicula in response["result"]

    def dar_informacion(self, pelicula: str) -> dict:
        req = requests.get(f"{self.base}/informacion?pelicula={pelicula}")
        exit_code = req.status_code
        response = req.json()

        return {"status-code": exit_code, "mensaje": response["result"]}

    def dar_informacion_aleatoria(self) -> dict:
        req = requests.get(f"{self.base}/aleatorio")
        exit_code = req.status_code
        response = req.json()

        if exit_code != 200:
            return {"status-code": exit_code, "mensaje": response["result"]}

        req = requests.get(response["result"])
        exit_code = req.status_code
        response = req.json()

        return {"status-code": exit_code, "mensaje": response["result"]}

    def agregar_informacion(
        self, pelicula: str, sinopsis: str, access_token: str
    ) -> str:
        req = requests.post(
            f"{self.base}/update",
            data={"pelicula": pelicula, "sinopsis": sinopsis},
            headers={"Authorization": access_token},
        )
        exit_code = req.status_code
        response = req.json()

        match exit_code:
            case 401:
                return "Agregar pelicula no autorizado"
            case 400:
                return response["result"]
            case _:
                return "La base de la API ha sido actualizada"

    def actualizar_informacion(
        self, pelicula: str, sinopsis: str, access_token: str
    ) -> str:
        req = requests.patch(
            f"{self.base}/update",
            data={"pelicula": pelicula, "sinopsis": sinopsis},
            headers={"Authorization": access_token},
        )
        exit_code = req.status_code
        response = req.json()

        match exit_code:
            case 401:
                return "Editar información no autorizado"
            case 200:
                return "La base de la API ha sido actualizada"
            case _:
                return response["result"]

    def eliminar_pelicula(self, pelicula: str, access_token: str) -> str:
        req = requests.delete(
            f"{self.base}/remove",
            data={"pelicula": pelicula},
            headers={"Authorization": access_token},
        )
        exit_code = req.status_code
        response = req.json()

        match exit_code:
            case 401:
                return "Eliminar pelicula no autorizado"
            case 200:
                return "La base de la API ha sido actualizada"
            case _:
                return response["result"]


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4444
    DATABASE = {
        "Mamma Mia": "Mamma Mia es una Comedia musical con ABBA",
        "Monsters Inc": "Monsters Inc trata sobre monstruos que asustan, niños y risas",
        "Incredibles": "Incredibles trata de una familia de superhéroes que salva el mundo",
        "Avengers": "Avengers trata de superhéroes que luchan contra villanos poderosos",
        "Titanic": "Titanic es sobre amor trágico en el hundimiento del Titanic",
        "Akira": "Akira es una película de ciencia ficción japonesa con poderes psíquicos",
        "High School Musical": "High School Musical es un drama musical adolescente en East High",
        "The Princess Diaries": "The Princess Diaries es sobre Mia, una joven que descubre que es"
        "princesa de Genovia",
        "Iron Man": "Iron Man trata sobre un hombre construye traje de alta tecnología "
        "para salvar al mundo",
        "Tarzan": "Tarzan es sobre un hombre criado por simios en la jungla",
        "The Pianist": "The Pianist es sobre un músico judío que sobrevive en Varsovia"
        " durante el Holocausto",
    }
    thread = api.Server(HOST, PORT, DATABASE)
    thread.start()

    peliculas = Peliculas(HOST, PORT)
    print(peliculas.saludar())
    print(peliculas.dar_informacion_aleatoria())
    print(
        peliculas.actualizar_informacion(
            "Titanic",
            "Titanic es sobre amor trágico inspitado"
            " en el historico hundimiento del Titanic",
            "tereiic2233",
        )
    )
    print(peliculas.verificar_informacion("Tarzan"))
    print(peliculas.dar_informacion("The Princess Diaries"))
    print(peliculas.dar_informacion("Monsters Inc"))
    print(
        peliculas.agregar_informacion(
            "Matilda",
            "Matilda es sobre una niña con poderes"
            "telequinéticos que enfrenta a su malvada directora",
            "tereiic2233",
        )
    )
    print(peliculas.dar_informacion("Matilda"))
