# pylint: disable=missing-docstring, E0611

import json
import sys

from frontend.start_window import LoginWindow
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":

    app = QApplication([])
    app.setApplicationName("DCConejoChico")

    with open("client.json", "r", encoding="utf-8") as file:
        client_host = json.load(file)["host"]
    client_port = int(sys.argv[1])

    login_window = LoginWindow(host=client_host, port=client_port)
    login_window.show()

    sys.exit(app.exec())
