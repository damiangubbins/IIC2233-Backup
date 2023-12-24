# pylint: disable=missing-docstring

import json
import socket
import sys
import threading

from funciones_servidor import decrypt, encrypt
from logger import Logger


class Server:

    def __init__(self, host: str, port: int):
        super().__init__()

        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.current_user: str | None = None

        self.bind_and_listen()
        self.accept_connections()

    def bind_and_listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Listening on {self.host}:{self.port}...")

    def accept_connections(self):
        thread = threading.Thread(target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self):
        print("Waiting for connections...\n")

        while True:
            client_socket, _ = self.socket.accept()
            Logger.first_line()
            Logger.log("client", "connect", "connected",
                       f"{client_socket.getsockname()}")
            listening_client_thread = threading.Thread(
                target=self.listen_client_thread,
                args=(client_socket,),
                daemon=True
            )
            listening_client_thread.start()

    @staticmethod
    def send(data, client_socket: socket.socket):

        if data != "":
            data = encrypt(data)
            for chunk in data:
                client_socket.sendall(chunk)

    def listen_client_thread(self, client_socket: socket.socket):
        Logger.log("server", "...", "listening",
                   f"{client_socket.getsockname()}")

        try:
            while True:
                response_bytes_length = client_socket.recv(4)
                response_length = int.from_bytes(
                    response_bytes_length, byteorder="big")
                response = bytearray()

                while len(response) < response_length:
                    client_socket.recv(4)
                    response.extend(client_socket.recv(36))

                received = decrypt(response.decode().strip("\x00"))

                if received != "":
                    Logger.log("server", "...", "received",
                               f"{received[:20]}...")
                    response = self.process_command(received)
                    Logger.log("server", "...", "sent",
                               f"{response[:20]}...")
                    self.send(response, client_socket)

        except ConnectionError:
            with open("server.json", "r+", encoding="utf-8") as f:
                server_json = json.load(f)

                if self.current_user is not None:
                    user_score = server_json["users"][self.current_user]["score"]

                    Logger.log(f"{self.current_user}", "disconnect",
                               "disconnected", f"score: {user_score}")

                    self.current_user = None

    def process_command(self, command: str) -> str:

        if "score:" in command:

            command = command.split(":")[1]
            user, level, score = command.split(",")

            if user in ("test1", "test2", "test3"):
                Logger.log(user, "score:", "received", "test user")
                return ""

            Logger.log(user, "score:", "received", "moving to next level")

            with open("server.json", "r+", encoding="utf-8") as f:
                server_json = json.load(f)

                if level == "3":
                    new_level = 1
                else:
                    new_level = int(level) + 1

                server_json["users"][user]["level"] = new_level
                Logger.log(user, "score:", "level changed", str(new_level))

                server_json["users"][user]["score"] += round(float(score), 2)
                Logger.log(user, "score:", "score increased",
                           str(round(float(score), 2)))

                f.seek(0)
                f.write(json.dumps(server_json))
                f.truncate()
                Logger.log("server", "...", "changes saved", "server.json")

            return ""

        if "verify:" in command:
            user = command.split(":")[1]

            with open("server.json", "r+", encoding="utf-8") as f:
                server_json = json.load(f)

                if user in server_json["banned_users"]:
                    Logger.log(user, "verify:", "ban check", "user is banned")
                    return f"user:{user},0"

                Logger.log(user, "verify:", "ban check", "user not banned")

                if user not in server_json["users"]:
                    server_json["users"][user] = {"level": 1, "score": 0.0}
                    Logger.log(user, "verify:", "user created",
                               "added to server.json")

                    f.seek(0)
                    f.write(json.dumps(server_json))
                    f.truncate()
                    Logger.log("server", "...", "changes saved", "server.json")

            self.current_user = user
            return f"user:{user},{server_json['users'][user]['level']}"

        if "ban:" in command:
            user = command.split(":")[1]

            with open("server.json", "r+", encoding="utf-8") as f:
                server_json = json.load(f)

                if user in server_json["banned_users"]:
                    Logger.log(user, "ban:", "ban check",
                               "user already banned")
                    return ""

                if user in server_json["users"]:
                    del server_json["users"][user]
                    Logger.log(user, "ban:", "user deleted",
                               "removed from server.json")

                server_json["banned_users"].append(user)
                Logger.log(user, "ban:", "user banned", "...")

                f.seek(0)
                f.write(json.dumps(server_json))
                f.truncate()
                Logger.log("server", "...", "changes saved", "server.json")

            return ""

        if "hall:" in command:

            with open("server.json", "r+", encoding="utf-8") as f:
                server_json = json.load(f)

                users = server_json["users"]
                hall_of_fame = sorted(
                    users.items(), key=lambda x: x[1]["score"], reverse=True)

                top_users = ""
                for user in hall_of_fame:
                    if user[1]["score"] == 0.0:
                        continue
                    top_user = f"{user[0]}-{user[1]['score']},"
                    top_users += top_user

            Logger.log("server", "hall:", "sent", "sorted users")
            return f"hall:{top_users}"

        return ""


if __name__ == "__main__":

    with open("server.json", "rt", encoding="utf-8") as file:
        server_host = json.load(file)["host"]
    server_port = int(sys.argv[1])

    server = Server(host=server_host, port=server_port)
