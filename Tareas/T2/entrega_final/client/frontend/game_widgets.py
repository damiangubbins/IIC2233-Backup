# pylint: disable=missing-docstring, E0611, E0401, W0212, C0103

import sys

import frontend.stylesheets as ss
import parametros as p
from backend.sprites import Carrot
from frontend.board import Board
from frontend.item_widgets import (AppleBombWidget, AppleItem, FireZoneWidget,
                                   FreezeBombWidget, FreezeItem, Heart,
                                   IceZoneWidget)
from frontend.sprite_widgets import (CannonWidget, CarrotWidget, Layer,
                                     RabbitWidget, WolfWidget)
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtGui import QKeyEvent, QMouseEvent, QPixmap, QTransform
from PyQt6.QtWidgets import (QAbstractItemView, QHBoxLayout, QLabel,
                             QListWidget, QPushButton, QStyledItemDelegate,
                             QStyleOptionViewItem, QVBoxLayout, QWidget)


class GameWindow(QWidget):

    key_signal = pyqtSignal(int)
    mouse_signal = pyqtSignal(int, int)
    carrot_spawn = pyqtSignal(int)
    pause_signal = pyqtSignal()
    kill_adds = pyqtSignal()
    infinity = pyqtSignal()

    def __init__(self, maze: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.maze_int = maze

        self.board = Board(maze)
        self.setLayout(self.board)

        self.setFixedWidth(p.ANCHO_LABERINTO * p.CELL_SIZE)

        self.layers: dict[int, Layer]
        self.set_layers()

        self.setFixedSize(p.ANCHO_LABERINTO * p.CELL_SIZE,
                          p.LARGO_LABERINTO * p.CELL_SIZE)

        self.rabbit: RabbitWidget

        self.wolf_widgets: dict[int, WolfWidget] = {}

        self.cannon_widgets: dict[int, CannonWidget] = {}

        self.carrots: dict[int, Carrot] = {}
        self.carrot_widgets: dict[int, CarrotWidget] = {}

        self.item_widgets: dict[int, AppleBombWidget | FreezeBombWidget] = {}

        self.fire_zone_widgets: dict[int, FireZoneWidget] = {}
        self.ice_zone_widgets: dict[int, IceZoneWidget] = {}

        self.pressed_keys = set()

        self.is_paused = False
        self.killed = False

    def set_layers(self):
        self.layers = {layer: Layer(layer, self) for layer in range(3)}

        self.layers[0].raise_()
        self.layers[1].stackUnder(self.layers[0])
        self.layers[2].stackUnder(self.layers[1])

        for layer in self.layers.values():
            layer.show()

    def place_rabbit(self, x, y):
        if self.maze_int == 1:
            self.rabbit = RabbitWidget(
                x*p.CELL_SIZE, (y - 2)*p.CELL_SIZE, self)
            direction = "RIGHT"
        else:
            self.rabbit = RabbitWidget(
                (x - 2)*p.CELL_SIZE, y*p.CELL_SIZE, self)
            direction = "DOWN"

        self.rabbit.raise_()
        self.rabbit.show()
        self.rabbit.entrance_animation(direction)

    def place_wolf(self, _id, _type, x, y):
        wolf = WolfWidget(_id, _type, self.maze_int, x *
                          p.CELL_SIZE, y*p.CELL_SIZE, self)
        self.wolf_widgets[_id] = wolf
        wolf.stackUnder(self.layers[0])
        wolf.show()

    def place_cannon(self, _id, _type, x, y):
        cannon = CannonWidget(_id, _type, x*p.CELL_SIZE, y*p.CELL_SIZE, self)
        self.cannon_widgets[_id] = cannon
        cannon.stackUnder(self.layers[0])
        cannon.show()

    def place_item(self, _id, _type, x, y):
        match _type:
            case "APPLE":
                item = AppleBombWidget(_id, x*p.CELL_SIZE, y*p.CELL_SIZE, self)
            case "FREEZE":
                item = FreezeBombWidget(
                    _id, x*p.CELL_SIZE, y*p.CELL_SIZE, self)
            case _:
                raise ValueError("Item type not recognized")
        self.item_widgets[_id] = item
        item.stackUnder(self.layers[1])
        item.show()

    def remove_item(self, _id):
        self.item_widgets[_id].deleteLater()
        del self.item_widgets[_id]

    def spawn_carrot(self, _id, x, y, direction):
        carrot = Carrot(_id, self.maze_int, direction, x, y)
        self.carrots[carrot._id] = carrot

        carrot_widget = CarrotWidget(
            carrot._id, direction, x*p.CELL_SIZE, y*p.CELL_SIZE, self)
        self.carrot_widgets[carrot._id] = carrot_widget

        carrot.animate.connect(carrot_widget._move)
        carrot.wall_colision.connect(carrot_widget.stop_movement)

        carrot_widget.stackUnder(self.layers[1])
        carrot_widget.show()

    def place_fire_zone(self, _id, x, y):
        fire_zone = FireZoneWidget(_id, x*p.CELL_SIZE, y*p.CELL_SIZE, self)
        self.fire_zone_widgets[_id] = fire_zone

        fire_zone.stackUnder(self.layers[2])
        fire_zone.show()

    def place_ice_zone(self, _id, x, y):
        ice_zone = IceZoneWidget(_id, x*p.CELL_SIZE, y*p.CELL_SIZE, self)
        self.ice_zone_widgets[_id] = ice_zone

        ice_zone.stackUnder(self.layers[2])
        ice_zone.show()

    def remove_fire_zone(self, _id):
        self.fire_zone_widgets[_id].deleteLater()
        del self.fire_zone_widgets[_id]

    def remove_ice_zone(self, _id):
        self.ice_zone_widgets[_id].deleteLater()
        del self.ice_zone_widgets[_id]

    def remove_wolf(self, _id):
        self.wolf_widgets[_id].hide()

    def slow_wolf(self, _id):
        self.wolf_widgets[_id].speed = int(
            p.MODIFIED_WOLF_SPEED[self.maze_int] * 1.33 * 0.90)

        self.wolf_widgets[_id].set_amimation_timer()
        self.wolf_widgets[_id].set_frame_timer()

    def normalize_wolves(self):
        for wolf in self.wolf_widgets.values():
            wolf.show()
            wolf.speed = int(p.MODIFIED_WOLF_SPEED[self.maze_int] * 0.90)
            wolf.set_amimation_timer()
            wolf.set_frame_timer()

    def pause(self):
        if not self.is_paused:
            for carrot in self.carrots.values():
                carrot.move_timer.stop()

            self.is_paused = True

        else:
            for carrot in self.carrots.values():
                carrot.move_timer.start()

            self.is_paused = False

    def remove_all(self):
        if not self.killed:
            for wolf in self.wolf_widgets.values():
                wolf.deleteLater()

            for cannon in self.cannon_widgets.values():
                cannon.deleteLater()

            self.killed = True

    def keyPressEvent(self, a0: QKeyEvent):
        if a0.isAutoRepeat():
            return

        self.pressed_keys.add(a0.key())

        if a0.key() == Qt.Key.Key_P and not self.rabbit.respawn_status:
            self.pause()
            self.pause_signal.emit()

        if (len({Qt.Key.Key_K, Qt.Key.Key_I, Qt.Key.Key_L}.intersection(self.pressed_keys)
                ) == 3):
            self.kill_adds.emit()
            self.remove_all()

        if (len({Qt.Key.Key_I, Qt.Key.Key_N, Qt.Key.Key_F}.intersection(self.pressed_keys)
                ) == 3):
            self.infinity.emit()

        if not self.rabbit.animation_status:
            key = a0.key()
            self.key_signal.emit(key)

    def keyReleaseEvent(self, a0: QKeyEvent):
        if a0.key() in self.pressed_keys:
            self.pressed_keys.remove(a0.key())

    def mousePressEvent(self, a0: QMouseEvent):
        self.mouse_signal.emit(a0.pos().y() // p.CELL_SIZE,
                               a0.pos().x() // p.CELL_SIZE)


class LeftMenu(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        side_menu = QVBoxLayout()
        self.setLayout(side_menu)

        self.setFixedWidth(150)

        self.time_label = QLabel("Time", self)
        self.time_label.setStyleSheet(ss.TEXT)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        side_menu.addWidget(self.time_label)

        self.time = QLabel("", self)
        self.time.setStyleSheet(ss.TEXT)
        self.time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        side_menu.addWidget(self.time)

        button_layout = QHBoxLayout()
        side_menu.addLayout(button_layout)

        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setStyleSheet(ss.NORMAL_BUTTON)
        self.exit_button.setFixedWidth(65)
        self.exit_button.clicked.connect(sys.exit)
        button_layout.addWidget(self.exit_button)

        self.pause_button = QPushButton("Pause", self)
        self.pause_button.setStyleSheet(ss.NORMAL_BUTTON)
        self.pause_button.setFixedWidth(65)
        button_layout.addWidget(self.pause_button)

        self.item_list = QListWidget(self)
        self.item_list.setStyleSheet(ss.INVENTORY)
        self.item_list.setFixedHeight(315)
        self.item_list.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection)
        self.item_list.setIconSize(QSize(48, 48))
        self.delegate = ItemDelegate()
        self.item_list.setItemDelegate(self.delegate)
        side_menu.addWidget(self.item_list)

        self.deselect_button = QPushButton("Deselect", self)
        self.deselect_button.setStyleSheet(ss.NORMAL_BUTTON)
        self.deselect_button.clicked.connect(self.item_list.clearSelection)
        side_menu.addWidget(self.deselect_button)

        self.score_label = QLabel("Score", self)
        self.score_label.setStyleSheet(ss.TEXT)
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        side_menu.addWidget(self.score_label)

        self.score = QLabel("0", self)
        self.score.setStyleSheet(ss.TEXT)
        self.score.setAlignment(Qt.AlignmentFlag.AlignCenter)
        side_menu.addWidget(self.score)

        self.next_level_button = QPushButton("Next Level", self)
        self.next_level_button.setStyleSheet(ss.NORMAL_BUTTON)
        self.next_level_button.setDisabled(True)
        side_menu.addWidget(self.next_level_button)

    def add_item(self, _id: int, _type: str):
        match _type:
            case "APPLE":
                item = AppleItem(_id)
            case "FREEZE":
                item = FreezeItem(_id)
            case _:
                raise ValueError("Item type not recognized")
        self.item_list.addItem(item)

    def remove_item(self):
        self.item_list.takeItem(self.item_list.currentRow())
        self.item_list.clearSelection()

    def update_time(self, time: int):
        self.time.setText(str(time))

    def update_score(self, score: float):
        self.score.setText(str(score))

    def switch_button(self):
        self.next_level_button.setEnabled(
            not self.next_level_button.isEnabled())


class RightMenu(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        side_menu = QVBoxLayout()
        self.setLayout(side_menu)

        self.setFixedWidth(100)

        self.heart_list = QListWidget(self)
        self.heart_list.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection)
        self.heart_list.setStyleSheet(ss.HP_BAR)
        self.heart_list.setIconSize(QSize(48, 48))
        self.delegate = ItemDelegate()
        self.heart_list.setItemDelegate(self.delegate)
        side_menu.addWidget(self.heart_list)

        self.logo = QPixmap(p.LOGO).scaledToHeight(70)
        self.transform = QTransform()
        self.transform.rotate(90)
        self.logo_label = QLabel()
        self.logo_label.setStyleSheet(ss.LOGO)
        self.logo_label.setPixmap(self.logo.transformed(self.transform))
        side_menu.addWidget(self.logo_label)

    def add_heart(self, quantity: int, _type: str):
        for _ in range(quantity):
            heart = Heart(_type)
            self.heart_list.addItem(heart)

    def remove_heart(self):
        self.heart_list.takeItem(self.heart_list.count() - 1)

    def infinity_mode(self):
        self.heart_list.clear()
        self.add_heart(1, "golden")


class ItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.decorationPosition = QStyleOptionViewItem.Position.Top
        super().paint(painter, option, index)


if __name__ == "__main__":
    pass
