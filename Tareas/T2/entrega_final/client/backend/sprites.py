# pylint: disable=missing-docstring, E0611, E0401

from random import choice

import parametros as p
from PyQt6.QtCore import QObject, QTimer, pyqtSignal


class Rabbit(QObject):

    animate = pyqtSignal(str, tuple)
    wall_colision = pyqtSignal()
    position = pyqtSignal(str, int, int, int)

    def __init__(
            self, maze: int, row: int, column: int, *args, hp: int = p.CANTIDAD_VIDAS, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.row = row
        self.column = column
        self.speed = p.VELOCIDAD_CONEJO

        self.hp: int
        self.hp = hp

        self.maze_int = maze
        self.maze: list[list[str]]
        self.get_maze()

        self.direction: str = "IDLE"

        self.move_timer = QTimer()
        self.move_timer.setInterval(int(1000/p.VELOCIDAD_CONEJO))
        self.move_timer.timeout.connect(self._move)

    def get_maze(self):
        with open(p.MAZES[self.maze_int], 'r', encoding="UTF-8") as f:
            maze = f.readlines()
            self.maze = [row.strip().split(",") for row in maze]
        if self.maze[-1] == [""]:
            self.maze.pop(-1)

    def get_direction(self, key):

        if key in p.DIRECTIONS:
            self.direction = p.DIRECTIONS[key]

            self._move()
            self.move_timer.start()

        return

    def _move(self):
        try:
            match self.direction:
                case "UP":
                    if self.maze[self.row - 1][self.column] != "P":
                        self.row = max(0, self.row - 1)
                        self.animate.emit(self.direction, (self.column * p.CELL_SIZE,
                                                           self.row * p.CELL_SIZE))
                    else:
                        self.move_timer.stop()
                        self.wall_colision.emit()

                case "DOWN":
                    if self.maze[self.row + 1][self.column] != "P":
                        self.row = min(15, self.row + 1)
                        self.animate.emit(self.direction, (self.column * p.CELL_SIZE,
                                                           self.row * p.CELL_SIZE))
                    else:
                        self.move_timer.stop()
                        self.wall_colision.emit()

                case "LEFT":
                    if self.maze[self.row][self.column - 1] != "P" and self.column > 0:
                        self.column = max(0, self.column - 1)
                        self.animate.emit(self.direction, (self.column * p.CELL_SIZE,
                                                           self.row * p.CELL_SIZE))
                    else:
                        self.move_timer.stop()
                        self.wall_colision.emit()

                case "RIGHT":
                    if self.maze[self.row][self.column + 1] != "P":
                        self.column = min(15, self.column + 1)
                        self.animate.emit(self.direction, (self.column * p.CELL_SIZE,
                                                           self.row * p.CELL_SIZE))
                    else:
                        self.move_timer.stop()
                        self.wall_colision.emit()

                case _:
                    return

        except IndexError:
            return

        self.position.emit("RABBIT", 0, self.row, self.column)


class Wolf(QObject):

    _id = 0
    animate = pyqtSignal(str, tuple)
    position = pyqtSignal(str, int, int, int)

    def __init__(self, maze: int, _type: str, row: int, column: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._id = Wolf._id
        Wolf._id += 1

        self._type = _type

        self.row = row
        self.column = column

        self.speed = p.MODIFIED_WOLF_SPEED[maze]
        self.move_timer: QTimer
        self.set_timer()
        self.is_slowed = False

        self.maze_int = maze
        self.maze: list[list[str]]
        self.get_maze()

        if self._type == "V":
            self.direction = choice(["UP", "DOWN"])
        else:
            self.direction = choice(["LEFT", "RIGHT"])

    def set_timer(self):
        self.move_timer = QTimer()
        self.move_timer.setInterval(self.speed)
        self.move_timer.timeout.connect(self._move)
        self.move_timer.start()

    def get_maze(self):
        with open(p.MAZES[self.maze_int], 'r', encoding="UTF-8") as f:
            maze = f.readlines()
            self.maze = [row.strip().split(",") for row in maze]

    def _move(self):
        match self.direction:
            case "UP":
                if self.maze[self.row - 1][self.column] != "P":
                    self.row = max(0, self.row - 1)
                else:
                    self.direction = "DOWN"

            case "DOWN":
                if self.maze[self.row + 1][self.column] != "P":
                    self.row = min(15, self.row + 1)
                else:
                    self.direction = "UP"

            case "LEFT":
                if self.maze[self.row][self.column - 1] != "P":
                    self.column = max(0, self.column - 1)
                else:
                    self.direction = "RIGHT"

            case "RIGHT":
                if self.maze[self.row][self.column + 1] != "P":
                    self.column = min(15, self.column + 1)
                else:
                    self.direction = "LEFT"

            case _:
                return

        self.animate.emit(self.direction, (self.column *
                          p.CELL_SIZE, self.row * p.CELL_SIZE))
        self.position.emit("WOLF", self._id, self.row, self.column)


class Cannon(QObject):
    "AKA carrot spawner"
    _id = 0
    spawn_carrot = pyqtSignal(int, int, int, str)

    def __init__(self, direction: str, row: int, column: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._id = Cannon._id
        Cannon._id += 1

        self.direction = direction

        self.row = row
        self.column = column

        self.shoot_carrot_timer = QTimer()
        self.shoot_carrot_timer.setInterval(2000)
        self.shoot_carrot_timer.timeout.connect(self.shoot_carrot)
        self.shoot_carrot_timer.start()

    def shoot_carrot(self):
        self.spawn_carrot.emit(self._id, self.row, self.column, self.direction)


class Carrot(QObject):

    animate = pyqtSignal(tuple)
    wall_colision = pyqtSignal(int)
    position = pyqtSignal(str, int, int, int)

    def __init__(self, _id: int, maze: int, direction: str, row: int, column: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._id = _id

        self.maze_int = maze
        self.maze: list[list[str]]
        self.get_maze()

        self.direction = direction

        self.row = row
        self.column = column

        self.speed = int(1000/p.VELOCIDAD_ZANAHORIA)

        self.move_timer = QTimer()
        self.move_timer.setInterval(self.speed)
        self.move_timer.timeout.connect(self._move)
        self.move_timer.start()

    def get_maze(self):
        with open(p.MAZES[self.maze_int], 'r', encoding="UTF-8") as f:
            maze = f.readlines()
            self.maze = [row.strip().split(",") for row in maze]

    def _move(self):
        match self.direction:
            case "UP":
                if self.maze[self.row - 1][self.column] != "P":
                    self.row = max(0, self.row - 1)
                    self.position.emit("CARROT", self._id,
                                       self.row, self.column)
                else:
                    self.wall_colision.emit(self._id)
                    self.position.emit("CARROT", self._id, -3, -3)

            case "DOWN":
                if self.maze[self.row + 1][self.column] != "P":
                    self.row = min(15, self.row + 1)
                    self.position.emit("CARROT", self._id,
                                       self.row, self.column)
                else:
                    self.wall_colision.emit(self._id)
                    self.position.emit("CARROT", self._id, -3, -3)

            case "LEFT":
                if self.maze[self.row][self.column - 1] != "P":
                    self.column = max(0, self.column - 1)
                    self.position.emit("CARROT", self._id,
                                       self.row, self.column)
                else:
                    self.wall_colision.emit(self._id)
                    self.position.emit("CARROT", self._id, -3, -3)

            case "RIGHT":
                if self.maze[self.row][self.column + 1] != "P":
                    self.column = min(15, self.column + 1)
                    self.position.emit("CARROT", self._id,
                                       self.row, self.column)
                else:
                    self.wall_colision.emit(self._id)
                    self.position.emit("CARROT", self._id, -3, -3)

            case _:
                return

        self.animate.emit((self.column * p.CELL_SIZE,
                           self.row * p.CELL_SIZE))


if __name__ == "__main__":
    pass
