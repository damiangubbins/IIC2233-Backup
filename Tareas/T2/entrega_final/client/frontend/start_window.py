# pylint: disable=missing-docstring, E0611, E0401

import sys

import frontend.stylesheets as ss
import parametros as p
from backend.client import Client
from backend.funciones_cliente import validacion_formato
from DCConejoChico import DCConejoChico
from PyQt6.QtCore import Qt, QUrl, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import (QHBoxLayout, QLabel, QLineEdit, QMessageBox,
                             QPushButton, QVBoxLayout, QWidget)


class LoginWindow(QWidget):

    def __init__(self, host: str, port: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.host = host
        self.port = port
        self.client = Client(self.host, self.port)
        self.client.thread.connection_lost.connect(self.connection_lost_popup)
        self.client.hall_of_fame.connect(self.set_hall_of_fame)
        self.client.verify.connect(self.start_game)

        self.game: DCConejoChico | None = None

        self.setWindowTitle("Login")
        self.setFixedWidth(600)

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setLoops(-2)
        self.player.setSource(QUrl.fromLocalFile(
            "assets_extra/Title - HoloCure Music.mp3"))
        self.audio_output.setVolume(0.1)
        self.player.play()

        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)

        self.logo_widget = LogoWidget()
        self._layout.addWidget(self.logo_widget)

        self.login_widget = LoginWidget()
        self.login_widget.login_signal.connect(self.request_verification)
        self.login_widget.ban_signal.connect(self.ban_user)
        self._layout.addWidget(self.login_widget)

        self.hall_of_fame_widget = HallOfFameWidget()
        self._layout.addWidget(self.hall_of_fame_widget)

        self.request_hall_of_fame()

    def request_hall_of_fame(self):
        self.client.send("hall:top5")

    def set_hall_of_fame(self, hall_of_fame: list):
        self.hall_of_fame_widget.remove_players()
        for i, player in enumerate(hall_of_fame):
            self.hall_of_fame_widget.add_player(i + 1, player[0], player[1])

    def request_verification(self, username: str):
        self.client.send(f"verify:{username}")

    def ban_user(self, username: str):
        self.client.send(f"ban:{username}")
        self.login_widget.label.setText("Banned.")
        self.request_hall_of_fame()

    def start_game(self, user: str, level: int):
        if level == 0:
            self.login_widget.label.setText("This user is banned.")
            self.login_widget.username_input.clear()
            return

        self.player.stop()
        self.close()

        self.game = DCConejoChico(self.client, user, level)
        self.game.start()

    def connection_lost_popup(self):
        QMessageBox.critical(self, "Connection lost",
                             "The connection to the server was lost.",
                             QMessageBox.StandardButton.Ok)
        sys.exit()


class LogoWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setContentsMargins(50, 0, 50, 0)
        self.setFixedHeight(100)

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self.logo = QPixmap(p.LOGO).scaledToWidth(500)
        self.logo_label = QLabel()
        self.logo_label.setStyleSheet(ss.LOGO)
        self.logo_label.setPixmap(self.logo)
        self.logo_label.setScaledContents(True)
        self._layout.addWidget(self.logo_label)


class LoginWidget(QWidget):

    login_signal = pyqtSignal(str)
    ban_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setContentsMargins(100, 0, 100, 0)
        self.setFixedHeight(250)

        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self.bunnies = QHBoxLayout()
        self.bunnies.setContentsMargins(0, 0, 0, 10)
        for i in [
            p.RABBIT["RIGHT"][2],
            p.CARROT["DOWN"],
            p.RABBIT["IDLE"][0],
            p.CARROT["DOWN"],
            p.RABBIT["LEFT"][2]
        ]:
            bunny = QPixmap(i)
            bunny_label = QLabel()
            bunny_label.setFixedSize(50, 50)
            bunny_label.setPixmap(bunny)
            bunny_label.setScaledContents(True)
            self.bunnies.addWidget(bunny_label)

        self._layout.addLayout(self.bunnies)

        self.label = QLabel("Welcome!")
        self.label.setStyleSheet(ss.TEXT)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self.label)

        self.username_input = QLineEdit()
        self.username_input.setStyleSheet(ss.TEXT_INPUT)
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self._layout.addWidget(self.username_input)

        self.buttons = QHBoxLayout()

        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet(ss.NORMAL_BUTTON)
        self.login_button.clicked.connect(self.verify_login)
        self.buttons.addWidget(self.login_button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.setStyleSheet(ss.NORMAL_BUTTON)
        self.exit_button.clicked.connect(sys.exit)
        self.buttons.addWidget(self.exit_button)

        self._layout.addLayout(self.buttons)

        self.wolves = QHBoxLayout()
        self.wolves.setContentsMargins(0, 10, 0, 0)
        for i in [
            p.WOLF["RIGHT"][2],
            p.CANNON["CU"],
            p.WOLF["UP"][0],
            p.CANNON["CU"],
            p.WOLF["LEFT"][2]
        ]:
            bunny = QPixmap(i)
            bunny_label = QLabel()
            bunny_label.setFixedSize(50, 50)
            bunny_label.setPixmap(bunny)
            bunny_label.setScaledContents(True)
            self.wolves.addWidget(bunny_label)

        self._layout.addLayout(self.wolves)

    def verify_login(self):

        username = self.username_input.text()

        if "score:" in username:
            self.ban_signal.emit(username.split(":")[1].split(",")[0])
            self.username_input.clear()
            return

        if not validacion_formato(username):
            self.label.setText("Invalid username.")
            self.username_input.clear()
            return

        self.login_signal.emit(self.username_input.text())


class HallOfFameWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._layout)

        self.setFixedHeight(250)
        self.setContentsMargins(100, 0, 100, 0)

        self.label = QLabel("Hall of Fame")
        self.label.setFixedHeight(40)
        self.label.setStyleSheet(ss.TEXT)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self.label)

        self.rankings = QVBoxLayout()
        self.rankings.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rankings.setSpacing(10)
        self._layout.addLayout(self.rankings)

    def add_player(self, rank: int, player: str, score: int):
        player_label = QLabel(f"{rank}. {player.ljust(16)} : {score}")
        player_label.setStyleSheet(ss.RANKING_LABEL)
        player_label.setFixedSize(350, 30)
        self.rankings.addWidget(player_label)

    def remove_players(self):
        for i in reversed(range(self.rankings.count())):
            self.rankings.itemAt(i).widget().setParent(None)


if __name__ == "__main__":
    pass
