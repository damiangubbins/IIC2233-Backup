# pylint: disable=missing-docstring, E0611, E0401

import parametros as p
from PyQt6.QtCore import QPoint, QPropertyAnimation, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel


class Layer(QLabel):

    def __init__(self, layer: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layer = layer

        self.setGeometry(0, 0, 0, 0)


class StaticElement(QLabel):

    def __init__(self, _type):
        super().__init__()

        if _type == "P":
            self.set_sprite(p.WALL)
        else:
            self.set_sprite(p.FLOOR)

    def set_sprite(self, sprite):
        self.setPixmap(QPixmap(sprite).scaled(p.CELL_SIZE, p.CELL_SIZE))
        self.setScaledContents(True)


class RabbitWidget(QLabel):

    exited = pyqtSignal()

    def __init__(self, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.current_direction = "IDLE"

        self.animation_value = 0
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(93)
        self.animation.finished.connect(self.stop_movement)

        self.animation_status = False
        self.respawn_status = False

        self.frame_timer = QTimer()
        self.frame_timer.setInterval(31)
        self.frame_timer.timeout.connect(self.update_frame)

        self.setGeometry(y, x, p.CELL_SIZE, p.CELL_SIZE)

        self.update_sprite(p.RABBIT["IDLE"][self.animation_value])

    def update_sprite(self, sprite):
        self.setPixmap(QPixmap(sprite).scaled(p.CELL_SIZE, p.CELL_SIZE))
        self.setScaledContents(True)

    def _move(self, direction, final_pos):
        self.current_direction = direction
        self.animation.setEndValue(QPoint(*final_pos))
        self.frame_timer.start()
        self.animation.start()
        self.animation_status = True

    def update_frame(self):
        self.update_sprite(
            p.RABBIT[self.current_direction][self.animation_value % 3]
        )
        self.animation_value += 1

    def stop_movement(self):
        self.animation_value = 0
        self.update_frame()
        self.frame_timer.stop()

    def wall_colision(self):
        self.animation_status = False

    def bunny_hit(self, row: int, column: int):
        self.respawn_status = True
        self.hide()
        QTimer().singleShot(250, lambda: self.respawn_animation(row, column))

    def respawn_animation(self, row: int, column: int):
        self.move(column * p.CELL_SIZE, row * p.CELL_SIZE)
        self.update_sprite(p.RABBIT["IDLE"][0])
        self.animation_status = False
        self.respawn_status = False
        self.show()
        QTimer().singleShot(250, self.hide)
        QTimer().singleShot(500, self.show)
        QTimer().singleShot(750, self.hide)
        QTimer().singleShot(1000, self.show)

    def entrance_animation(self, direction: str):

        self.animation_status = True
        self.animation.setDuration(500)

        if direction == "DOWN":
            self._move("DOWN", (self.x(), self.y() + p.CELL_SIZE*2))
        elif direction == "RIGHT":
            self._move("RIGHT", (self.x() + p.CELL_SIZE*2, self.y()))

        QTimer.singleShot(1000, lambda: self.animation.setDuration(93))
        QTimer.singleShot(
            1000, lambda: setattr(self, "animation_status", False))

    def exit_animation(self):
        self.animation_status = True
        self.animation.setDuration(500)

        if self.current_direction == "DOWN":
            self._move("DOWN", (self.x(), self.y() + p.CELL_SIZE*2))
        elif self.current_direction == "RIGHT":
            self._move("RIGHT", (self.x() + p.CELL_SIZE*2, self.y()))

        QTimer.singleShot(1000, self.exited.emit)
        QTimer.singleShot(1000, lambda: self.animation.setDuration(93))
        QTimer.singleShot(
            1000, lambda: setattr(self, "animation_status", False))


class WolfWidget(QLabel):

    def __init__(self, _id, _type, maze: int, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._id = _id
        self._type = _type

        self.current_direction: str
        self.speed = int(p.MODIFIED_WOLF_SPEED[maze] * 0.9)

        self.animation_value: int
        self.animation: QPropertyAnimation
        self.set_amimation_timer()

        self.frame_timer: QTimer
        self.set_frame_timer()

        self.setGeometry(y, x, p.CELL_SIZE, p.CELL_SIZE)

    def set_amimation_timer(self):
        self.animation_value = 0
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(self.speed)
        self.animation.finished.connect(self.stop_movement)

    def set_frame_timer(self):
        self.frame_timer = QTimer()
        self.frame_timer.setInterval(int(self.speed / 3))
        self.frame_timer.timeout.connect(self.update_frame)

    def update_sprite(self, sprite):
        self.setPixmap(QPixmap(sprite).scaled(p.CELL_SIZE, p.CELL_SIZE))
        self.setScaledContents(True)

    def _move(self, direction, final_pos):
        self.current_direction = direction
        self.animation.setEndValue(QPoint(*final_pos))
        self.frame_timer.start()
        self.animation.start()

    def update_frame(self):
        self.update_sprite(
            p.WOLF[self.current_direction][self.animation_value % 3]
        )
        self.animation_value += 1

    def stop_movement(self):
        self.animation_value = 0
        self.update_frame()
        self.frame_timer.stop()


class CannonWidget(QLabel):

    def __init__(self, _id, _type, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._id = _id
        self._type = _type

        self.setGeometry(y, x, p.CELL_SIZE, p.CELL_SIZE)

        self.update_sprite(p.CANNON[self._type])

    def update_sprite(self, sprite):
        self.setPixmap(QPixmap(sprite).scaled(p.CELL_SIZE, p.CELL_SIZE))
        self.setScaledContents(True)


class CarrotWidget(QLabel):

    def __init__(self, _id, direction, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._id = _id
        self.direction = direction

        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(111)

        self.setGeometry(y, x, p.CELL_SIZE, p.CELL_SIZE)

        self.update_sprite(p.CARROT[self.direction])

    def update_sprite(self, sprite):
        self.setPixmap(QPixmap(sprite).scaled(p.CELL_SIZE, p.CELL_SIZE))
        self.setScaledContents(True)

    def _move(self, final_pos):
        self.animation.setEndValue(QPoint(*final_pos))
        self.animation.start()

    def stop_movement(self, _id):
        self.deleteLater()
        del self


if __name__ == "__main__":
    pass
