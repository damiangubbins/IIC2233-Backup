import requests

import api


class Yolanda:

    def __init__(self, host, port):
        self.base = f"http://{host}:{port}"
        self.regex_validador_fechas = r'^(\d{1}|\d{2})\b\s+de\s+\w[a-zA-Z]+\s+de\s+\b((19|20)\d{2}|\d{2})$'
        self.regex_extractor_signo = r'(?:Las|Los)\s+(\w+(?:s|S))\s+(?:pueden\s+[\x00-\xFA]+\.)$'

    def saludar(self) -> dict:
        req = requests.get(self.base, timeout=1)
        data = req.json()
        return {"status-code": req.status_code, "saludo": data["result"]}

    def verificar_horoscopo(self, signo: str) -> bool:
        signos = requests.get(f"{self.base}/signos",
                              timeout=1).json()["result"]
        if signo in signos:
            return True

        return False

    def dar_horoscopo(self, signo: str) -> dict:
        params = {"signo": signo}
        req = requests.get(f"{self.base}/horoscopo", params=params, timeout=1)
        data = req.json()
        return {"status-code": req.status_code, "mensaje": data["result"]}

    def dar_horoscopo_aleatorio(self) -> dict:
        req = requests.get(f"{self.base}/aleatorio", timeout=1)
        data = req.json()

        match req.status_code:
            case 200:
                req = requests.get(data["result"], timeout=1)
                data = req.json()
                return {"status-code": req.status_code, "mensaje": data["result"]}
            case _:
                return {"status-code": req.status_code, "mensaje": data["result"]}

    def agregar_horoscopo(self, signo: str, mensaje: str, access_token: str) -> str:
        req = requests.post(
            f"{self.base}/update",
            headers={"AUTHORIZATION": access_token},
            data={"signo": signo, "mensaje": mensaje},
            timeout=1)
        data = req.json()

        match req.status_code:
            case 401:
                return "Agregar horóscopo no autorizado"
            case 400:
                return data["result"]
            case _:
                return "La base de YolandAPI ha sido actualizada"

    def actualizar_horoscopo(self, signo: str, mensaje: str, access_token: str) -> str:
        req = requests.put(
            f"{self.base}/update",
            headers={"AUTHORIZATION": access_token},
            data={"signo": signo, "mensaje": mensaje},
            timeout=1)
        data = req.json()

        match req.status_code:
            case 401:
                return "Editar horóscopo no autorizado"
            case 400:
                return data["result"]
            case _:
                return "La base de YolandAPI ha sido actualizada"

    def eliminar_signo(self, signo: str, access_token: str) -> str:
        req = requests.delete(
            f"{self.base}/remove",
            headers={"AUTHORIZATION": access_token},
            data={"signo": signo},
            timeout=1)
        data = req.json()

        match req.status_code:
            case 401:
                return "Eliminar signo no autorizado"
            case 400:
                return data["result"]
            case _:
                return "La base de YolandAPI ha sido actualizada"


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4444
    DATABASE = {
        "acuario": "Hoy será un hermoso día",
        "leo": "No salgas de casa.... te lo recomiendo",
    }
    thread = api.Server(HOST, PORT, DATABASE)
    thread.start()

    yolanda = Yolanda(HOST, PORT)
    print(yolanda.saludar())
    print(yolanda.dar_horoscopo_aleatorio())
    print(yolanda.verificar_horoscopo("acuario"))
    print(yolanda.verificar_horoscopo("pokemon"))
    print(yolanda.dar_horoscopo("acuario"))
    print(yolanda.dar_horoscopo("pokemon"))
    print(yolanda.agregar_horoscopo("a", "aaaaa", "pepaiic2233"))
    print(yolanda.dar_horoscopo("a"))
