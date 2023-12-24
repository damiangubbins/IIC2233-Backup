# pylint: disable=missing-docstring, E0611, E0401

import parametros as p
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QLabel, QListWidgetItem


class AppleBombWidget(QLabel):

    def __init__(self, _id, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._id = _id

        self.setGeometry(y, x, p.CELL_SIZE, p.CELL_SIZE)

        self.update_sprite(p.APPLE_BOMB)

    def update_sprite(self, sprite):
        self.setPixmap(QPixmap(sprite).scaled(p.CELL_SIZE, p.CELL_SIZE))
        self.setScaledContents(True)


class FreezeBombWidget(QLabel):

    def __init__(self, _id, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._id = _id

        self.setGeometry(y, x, p.CELL_SIZE, p.CELL_SIZE)

        self.update_sprite(p.FREEZE_BOMB)

    def update_sprite(self, sprite):
        self.setPixmap(QPixmap(sprite).scaled(p.CELL_SIZE, p.CELL_SIZE))
        self.setScaledContents(True)


class FireZoneWidget(QLabel):

    def __init__(self, _id, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._id = _id

        self.setGeometry(y, x, p.CELL_SIZE, p.CELL_SIZE)

        self.update_sprite(p.FIRE_ZONE)

    def update_sprite(self, sprite):
        self.setPixmap(QPixmap(sprite).scaled(p.CELL_SIZE, p.CELL_SIZE))
        self.setScaledContents(True)


class IceZoneWidget(QLabel):

    def __init__(self, _id, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._id = _id

        self.setGeometry(y, x, p.CELL_SIZE, p.CELL_SIZE)

        self.update_sprite(p.ICE_ZONE)

    def update_sprite(self, sprite):
        self.setPixmap(QPixmap(sprite).scaled(p.CELL_SIZE, p.CELL_SIZE))
        self.setScaledContents(True)


class AppleItem(QListWidgetItem):

    def __init__(self, _id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._id = _id
        self.setIcon(QIcon(p.APPLE_BOMB))


class FreezeItem(QListWidgetItem):

    def __init__(self, _id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._id = _id
        self.setIcon(QIcon(p.FREEZE_BOMB))


class Heart(QListWidgetItem):

    def __init__(self, _type: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if _type == "normal":
            self.setIcon(QIcon(p.HEART))
        else:
            self.setIcon(QIcon(p.GOLDEN_HEART))

        self.setFlags(~Qt.ItemFlag.ItemIsEditable)


if __name__ == '__main__':
    pass
