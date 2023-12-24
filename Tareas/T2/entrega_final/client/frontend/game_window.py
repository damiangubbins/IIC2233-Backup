# pylint: disable=missing-docstring, E0611, C0103, W0212, E0401

import sys

import parametros as p
from frontend.game_widgets import GameWindow, LeftMenu, RightMenu
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer, QSoundEffect
from PyQt6.QtWidgets import QHBoxLayout, QMessageBox, QWidget


class FullWindow(QWidget):

    def __init__(self, maze: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._layout = QHBoxLayout()
        self.setLayout(self._layout)

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setLoops(-2)
        self.player.setSource(QUrl.fromLocalFile(
            "assets_extra/Grassy Plains (Stage 1) - HoloCure.mp3"))
        self.audio_output.setVolume(0.1)
        self.player.play()

        self.game_window = GameWindow(maze, self)
        self.left_menu = LeftMenu(self)
        self.right_menu = RightMenu(self)

        self._layout.addWidget(self.left_menu)
        self._layout.addWidget(self.game_window)
        self._layout.addWidget(self.right_menu)
        self.game_window.setFocus()

        self.error_sound = QSoundEffect()
        self.error_sound.setSource(QUrl.fromLocalFile(p.ERROR))
        self.error_sound.setVolume(0.2)

    def change_game_widget(self, new_maze: int):
        new_game_window = GameWindow(new_maze, self)

        self._layout.replaceWidget(self.game_window, new_game_window)
        self.game_window = new_game_window
        self.game_window.setFocus()

    def victory_popup(self):
        self.player.stop()
        victory_sound = QSoundEffect()
        victory_sound.setSource(QUrl.fromLocalFile(p.VICTORY))
        victory_sound.setVolume(0.2)
        victory_sound.play()
        QMessageBox.information(self, "Victory",
                                "You have completed the game.",
                                QMessageBox.StandardButton.Ok)
        sys.exit()

    def game_over_popup(self):
        self.player.stop()
        defeat_sound = QSoundEffect()
        defeat_sound.setSource(QUrl.fromLocalFile(p.DEFEAT))
        defeat_sound.setVolume(0.2)
        defeat_sound.play()
        QMessageBox.information(self, "Defeat",
                                "You lost.",
                                QMessageBox.StandardButton.Ok)
        sys.exit()


if __name__ == "__main__":
    pass
