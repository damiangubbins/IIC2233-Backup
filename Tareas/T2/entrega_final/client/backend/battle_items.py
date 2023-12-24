# pylint: disable=missing-docstring, E0611, E0401

from dataclasses import dataclass, field
from itertools import count

import parametros as p
from PyQt6.QtCore import QObject, pyqtSignal


class Item(QObject):

    _id = 0
    use_signal = pyqtSignal(int, list)

    def __init__(self, maze: int, row: int, column: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._id = Item._id
        Item._id += 1

        self.row = row
        self.column = column

        self.maze_int = maze
        self.maze: list[list[str]]
        self.get_maze()

    def get_maze(self):
        with open(p.MAZES[self.maze_int], 'r', encoding="UTF-8") as f:
            maze = f.readlines()
            self.maze = [row.strip().split(",") for row in maze]

    def use(self, row: int, column: int) -> None:

        affected_cells: list[tuple[int, int]] = [(row, column)]

        if self.maze[row][column] == "P":
            self.use_signal.emit(self._id, [])
            return

        for i in range(1, 16 - row):
            if self.maze[row + i][column] != "P":
                affected_cells.append((row + i, column))
            else:
                break

        for i in range(1, row + 1):
            if self.maze[row - i][column] != "P":
                affected_cells.append((row - i, column))
            else:
                break

        for i in range(1, 16 - column):
            if self.maze[row][column + i] != "P":
                affected_cells.append((row, column + i))
            else:
                break

        for i in range(1, column + 1):
            if self.maze[row][column - i] != "P":
                affected_cells.append((row, column - i))
            else:
                break

        self.use_signal.emit(self._id, affected_cells)


class AppleBomb(Item):

    def __init__(self, maze: int, row: int, column: int, *args, **kwargs):
        Item.__init__(self, maze, row, column, *args, **kwargs)


class FreezeBomb(Item):

    def __init__(self, maze: int, row: int, column: int, *args, **kwargs):
        Item.__init__(self, maze, row, column, *args, **kwargs)


@dataclass
class FireZone:

    row: int
    column: int
    _id: int = field(default_factory=count().__next__, init=False)


@dataclass
class IceZone:

    row: int
    column: int
    _id: int = field(default_factory=count().__next__, init=False)


if __name__ == "__main__":
    pass
