# pylint: disable=missing-docstring, E0611

import sys

from frontend.start_window import LoginWindow
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":

    app = QApplication([])
    app.setApplicationName("DCConejoChico")

    client_host = sys.argv[1]
    client_port = int(sys.argv[2])

    login_window = LoginWindow(host=client_host, port=client_port)
    login_window.show()

    sys.exit(app.exec())
