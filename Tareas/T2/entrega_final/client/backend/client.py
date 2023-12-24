# pylint: disable=missing-docstring, E0611, E0401

import socket
import sys

from backend.funciones_servidor import decrypt, encrypt
from PyQt6.QtCore import QObject, QThread, pyqtSignal


class ListenThread(QThread):

    connection_lost = pyqtSignal()
    msg_signal = pyqtSignal(str)

    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket

    def run(self):
        try:
            while True:
                response_bytes_length = self.client_socket.recv(4)
                response_length = int.from_bytes(
                    response_bytes_length, byteorder="big")
                response = bytearray()

                while len(response) < response_length:
                    self.client_socket.recv(4)
                    response.extend(self.client_socket.recv(36))

                received = decrypt(response.decode().strip("\x00"))

                self.msg_signal.emit(received)

        except ConnectionError:
            self.connection_lost.emit()


class Client(QObject):

    verify = pyqtSignal(str, int)
    hall_of_fame = pyqtSignal(list)

    def __init__(self, host: str, port: int) -> None:
        super().__init__()
        self.thread: ListenThread | None = None
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

        try:
            self.connect_to_server()
            self.listen()
        except ConnectionError:
            print(f"No conection found on {self.host}:{self.port}.")
            self.client_socket.close()
            sys.exit()

    def connect_to_server(self):
        self.client_socket.connect((self.host, self.port))
        print("Client connected to server.")

    def listen(self):
        self.thread = ListenThread(self.client_socket)
        self.thread.msg_signal.connect(self.process_msg)
        self.thread.start()

    def send(self, msg: str):
        encrypted_msg = encrypt(msg)
        for block in encrypted_msg:
            self.client_socket.sendall(block)

    def process_msg(self, msg: str):

        if "hall:" in msg:
            msg = msg.split("hall:")[1]
            users = msg.split(",")
            users = [user.split("-") for user in users if user != ""]

            self.hall_of_fame.emit(users[:5])

        if "user:" in msg:
            msg = msg.split("user:")[1]

            user, level = msg.split(",")
            self.verify.emit(user, int(level))


if __name__ == "__main__":
    pass
