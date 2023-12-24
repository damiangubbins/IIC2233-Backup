# pylint: disable=missing-docstring, E0611, E0401

import parametros as p
from frontend.sprite_widgets import StaticElement
from PyQt6.QtWidgets import QGridLayout


class Board(QGridLayout):

    def __init__(self, maze: int):
        super().__init__()
        self.maze = maze
        self.init_gui()

    def init_gui(self):
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        with open(p.MAZES[self.maze], 'r', encoding="UTF-8") as f:
            maze = f.read().split(",")
            maze = [sprite.strip() for sprite in maze]

        positions = [(i, j) for i in range(p.ANCHO_LABERINTO)
                     for j in range(p.LARGO_LABERINTO)]

        for position, sprite in zip(positions, maze):
            self.addWidget(StaticElement(sprite), *position)


if __name__ == '__main__':
    pass
