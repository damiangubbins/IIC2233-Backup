# pylint: disable=missing-docstring, E0611, W0212, W0102, E0401

from copy import deepcopy

import parametros as p
from backend.battle_items import AppleBomb, FireZone, FreezeBomb, IceZone
from backend.sprites import Cannon, Carrot, Rabbit, Wolf
from frontend.item_widgets import AppleItem, FreezeItem
from PyQt6.QtCore import QObject, Qt, QTimer, pyqtSignal


class GameEngine(QObject):

    spawn_rabbit = pyqtSignal(int, int, int)
    spawn_wolf = pyqtSignal(int, str, int, int)
    spawn_cannon = pyqtSignal(int, str, int, int)

    place_item = pyqtSignal(int, str, int, int)
    remove_item = pyqtSignal(int)

    bunny_hit = pyqtSignal(int, int)

    place_fire_zone = pyqtSignal(int, int, int)
    place_ice_zone = pyqtSignal(int, int, int)

    remove_fire_zone = pyqtSignal(int)
    remove_ice_zone = pyqtSignal(int)

    remove_wolf = pyqtSignal(int)
    slow_wolf = pyqtSignal(int)
    normalize_wolves = pyqtSignal()

    add_to_inventory = pyqtSignal(int, str)
    remove_from_inventory = pyqtSignal()
    placement_error = pyqtSignal()

    tick = pyqtSignal(int)
    score = pyqtSignal(float)

    exit_animation = pyqtSignal()
    change_score = pyqtSignal(str)
    next_level = pyqtSignal(str, int, int, list)
    game_over = pyqtSignal()

    add_heart = pyqtSignal(int, str)
    remove_heart = pyqtSignal()

    def __init__(
        self,
        user_name: str,
        maze: int,
        *args,
        rabbit_hp: int | None = None,
        past_items: list[str] = [],
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.user_name = user_name
        self.maze_int = maze
        self.maze: list[list[str]]
        self.entrance: tuple[int, int]
        self.exit: tuple[int, int]
        self.get_maze()

        self.rabbit: Rabbit
        self.wolves: dict[int, Wolf] = {}
        self.cannons: dict[int, Cannon] = {}
        self.carrots: dict[int, Carrot] = {}

        self.positions = dict(deepcopy(p.POSITIONS))

        self._items: dict[int, AppleBomb | FreezeBomb] = {}
        self.player_items: dict[int, AppleBomb | FreezeBomb] = {}
        self.past_items = past_items

        self.fire_zones: dict[int, tuple[int, int]] = {}
        self.ice_zones: dict[int, tuple[int, int]] = {}

        self.wolf_hit_detection_timer = QTimer()
        self.wolf_hit_detection_timer.setInterval(100)
        self.wolf_hit_detection_timer.timeout.connect(self.wolf_hit_detection)

        self.killed_wolves: int = 0

        self.hit_detection_disabled = False
        self.killed = False
        self.infinity = False

        self.selected_item: AppleItem | FreezeItem | bool = False

        self.is_paused = False

        self.time_left = p.MODIFIED_LEVEL_TIME[maze]

        self.clock = QTimer()
        self.clock.setInterval(1000)
        self.clock.timeout.connect(self.clock_tick)
        self.clock.start()

        self.__post_init__(rabbit_hp)

    def __post_init__(self, rabbit_hp: int | None):
        if rabbit_hp is None:
            self.rabbit_hp = max(1, p.CANTIDAD_VIDAS - self.maze_int + 1)
        else:
            self.rabbit_hp = rabbit_hp

    def get_maze(self):
        with open(p.MAZES[self.maze_int], 'r', encoding="UTF-8") as f:
            maze = f.readlines()
            self.maze = [row.strip().split(",") for row in maze]

        self.entrance = [(row, column) for row in range(16)
                         for column in range(16) if self.maze[row][column] == "E"][0]

        self.exit = [(row, column) for row in range(16)
                     for column in range(16) if self.maze[row][column] == "S"][0]

    def instance_sprites(self):
        self.rabbit = Rabbit(self.maze_int, 1, 1, hp=self.rabbit_hp)
        self.spawn_rabbit.emit(1, 1, self.maze_int)

        for row in range(16):
            for column in range(16):

                sprite = self.maze[row][column]

                if sprite in p.TRANSLATOR["WOLF"]:
                    wolf = Wolf(
                        self.maze_int,
                        p.TRANSLATOR["WOLF"][sprite],
                        row,
                        column,
                    )
                    self.wolves[wolf._id] = wolf
                    self.spawn_wolf.emit(
                        wolf._id, wolf._type, row, column
                    )

                elif sprite in p.TRANSLATOR["CANNON"]:
                    cannon = Cannon(
                        p.TRANSLATOR["CANNON"][sprite],
                        row,
                        column,
                    )
                    self.cannons[cannon._id] = cannon
                    self.spawn_cannon.emit(cannon._id, sprite, row, column)

                elif sprite == "BM":
                    apple_bomb = AppleBomb(self.maze_int, row, column)
                    self._items[apple_bomb._id] = apple_bomb
                    self.place_item.emit(
                        apple_bomb._id, "APPLE", row, column
                    )

                elif sprite == "BC":
                    freeze_bomb = FreezeBomb(self.maze_int, row, column)
                    self._items[freeze_bomb._id] = freeze_bomb
                    self.place_item.emit(
                        freeze_bomb._id, "FREEZE", row, column
                    )

    def instance_carrot(self, _id: int, row: int, column: int, direction: str):
        self.carrots[_id] = Carrot(_id, self.maze_int, direction, row, column)
        self.carrots[_id].position.connect(self.update_positions)
        self.update_positions("CARROT", _id, row, column)

    def update_positions(self, sprite: str, _id: int, row: int, column: int):
        if sprite == "RABBIT":
            self.positions[sprite] = (row, column)
        else:
            self.positions[sprite][_id] = (row, column)

        self.hit_detection()

        if self.positions["RABBIT"] == self.exit:
            self.clock.stop()
            self.rabbit.move_timer.stop()
            self.exit_animation.emit()
            self.change_score.emit(
                f"score:{self.user_name},{self.maze_int},{self.get_round_score()}")
            self.positions["RABBIT"] = (-1, -1)

    def hit_detection(self):
        if self.hit_detection_disabled:
            return

        enemies = list(self.positions["WOLF"].values()) + \
            list(self.positions["CARROT"].values())

        if self.positions["RABBIT"] in enemies:
            self.respawn()

    def respawn(self):
        self.time_left = p.MODIFIED_LEVEL_TIME[self.maze_int]

        for wolf in self.wolves.values():
            if not wolf.move_timer.isActive():
                wolf.move_timer.start()
            wolf.speed = int(
                p.MODIFIED_WOLF_SPEED[self.maze_int])
            wolf.set_timer()
            wolf.is_slowed = False
        self.normalize_wolves.emit()

        self.rabbit.move_timer.stop()

        if not self.infinity:
            self.rabbit.hp -= 1
            self.remove_heart.emit()

        self.bunny_hit.emit(*self.entrance)
        self.rabbit.row, self.rabbit.column = self.entrance
        self.positions["RABBIT"] = self.entrance

        if self.rabbit.hp == 0:
            self.game_over.emit()

    def grab_item(self, key):
        if key == Qt.Key.Key_G.value:

            for _id, item in self._items.items():
                if (self.rabbit.row, self.rabbit.column) == (item.row, item.column):

                    if isinstance(item, AppleBomb):
                        self.add_to_inventory.emit(item._id, "APPLE")
                        item.use_signal.connect(self.use_apple_bomb)
                    else:
                        self.add_to_inventory.emit(item._id, "FREEZE")
                        item.use_signal.connect(self.use_freeze_bomb)

                    self._items.pop(_id)
                    self.player_items[_id] = item
                    self.remove_item.emit(_id)
                    break

    def use_apple_bomb(self, _id: int, affected_cells: list[tuple[int, int]]):
        self.player_items.pop(_id)
        ids = []
        for row, column in affected_cells:
            fire_zone = FireZone(row, column)
            self.fire_zones[fire_zone._id] = (row, column)
            self.place_fire_zone.emit(fire_zone._id, row, column)
            ids.append(fire_zone._id)

            self.wolf_hit_detection_timer.start()

        QTimer().singleShot(p.TIEMPO_BOMBA*1000, lambda: self.delete_fire_zone(ids))
        QTimer().singleShot(p.TIEMPO_BOMBA*1000, self.wolf_hit_detection_timer.stop)

        self.selected_item = False

    def use_freeze_bomb(self, _id: int, affected_cells: list[tuple[int, int]]):
        self.player_items.pop(_id)
        ids = []
        for row, column in affected_cells:
            ice_zone = IceZone(row, column)
            self.ice_zones[ice_zone._id] = (row, column)
            self.place_ice_zone.emit(ice_zone._id, row, column)
            ids.append(ice_zone._id)

            self.wolf_hit_detection_timer.start()

        QTimer().singleShot(p.TIEMPO_BOMBA*1000, lambda: self.delete_ice_zone(ids))
        QTimer().singleShot(p.TIEMPO_BOMBA*1000, self.wolf_hit_detection_timer.stop)

        self.selected_item = False

    def delete_fire_zone(self, _ids: list):
        for _id in _ids:
            self.fire_zones.pop(_id)
            self.remove_fire_zone.emit(_id)

    def delete_ice_zone(self, _ids: list):
        for _id in _ids:
            self.ice_zones.pop(_id)
            self.remove_ice_zone.emit(_id)

    def wolf_hit_detection(self):
        for _id, wolf in self.wolves.items():
            if (wolf.row, wolf.column) in self.fire_zones.values() and wolf.move_timer.isActive():
                wolf.move_timer.stop()
                self.remove_wolf.emit(_id)
                self.positions["WOLF"][_id] = (-2, -2)
                self.killed_wolves += 1
                break

            if (wolf.row, wolf.column) in self.ice_zones.values() and not wolf.is_slowed:
                self.slow_wolf.emit(_id)
                wolf.speed = int(
                    p.MODIFIED_WOLF_SPEED[self.maze_int] * 1.33)
                wolf.set_timer()
                wolf.is_slowed = True

    def select_item(self, item: AppleItem | FreezeItem | bool):
        self.selected_item = item

    def use_item(self, row: int, column: int):
        if not self.selected_item:
            return

        if self.maze[row][column] == "P":
            self.placement_error.emit()
            return

        if isinstance(self.selected_item, AppleItem | FreezeItem):
            self.player_items[self.selected_item._id].use(row, column)

        self.remove_from_inventory.emit()

    def add_items_to_inventory(self):

        for item in self.past_items:
            if item == "APPLE":
                new_item = AppleBomb(self.maze_int, 0, 0)
                self.player_items[new_item._id] = new_item
                new_item.use_signal.connect(self.use_apple_bomb)
                self.add_to_inventory.emit(new_item._id, "APPLE")
            else:
                new_item = FreezeBomb(self.maze_int, 0, 0)
                self.player_items[new_item._id] = new_item
                new_item.use_signal.connect(self.use_freeze_bomb)
                self.add_to_inventory.emit(new_item._id, "FREEZE")

    def pause(self):

        if not self.is_paused:
            self.rabbit.move_timer.stop()
            for wolf in self.wolves.values():
                wolf.move_timer.stop()
            for cannon in self.cannons.values():
                cannon.shoot_carrot_timer.stop()
            for carrot in self.carrots.values():
                carrot.move_timer.stop()
            self.clock.stop()

        else:
            self.rabbit.move_timer.start()
            for wolf in self.wolves.values():
                wolf.move_timer.start()
            for cannon in self.cannons.values():
                cannon.shoot_carrot_timer.start()
            for carrot in self.carrots.values():
                carrot.move_timer.start()
            self.clock.start()

        self.is_paused = not self.is_paused

    def clock_tick(self):
        self.time_left -= 1
        self.tick.emit(self.time_left)
        self.score.emit(self.get_round_score())

        if self.time_left == 0:
            self.respawn()

    def get_round_score(self):
        if self.infinity:
            return 350

        try:
            return self.killed_wolves * p.PUNTAJE_LOBO + round(
                (self.time_left * self.rabbit.hp) /
                (self.killed_wolves * p.PUNTAJE_LOBO),
                2)

        except ZeroDivisionError:
            return float(0)

    def prep_next_level(self):
        items = []
        for item in self.player_items.values():
            items.append("APPLE" if isinstance(
                item, AppleBomb) else "FREEZE")

        self.next_level.emit(
            self.user_name, self.maze_int + 1, self.rabbit.hp, items)

    def add_hearts(self):
        self.add_heart.emit(self.rabbit_hp, "normal")

    def k_i_l(self):
        self.hit_detection_disabled = True
        if not self.killed:
            del self.wolves
            del self.cannons
            del self.carrots
            self.killed = True

    def i_n_f(self):
        self.infinity = True
        self.clock_tick()
        self.clock.stop()


if __name__ == "__main__":
    pass
