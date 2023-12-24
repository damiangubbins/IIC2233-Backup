# pylint: disable=missing-docstring, E0611, W0212, C0103


from backend.client import Client
from backend.game import GameEngine
from frontend.game_window import FullWindow
from PyQt6.QtCore import QObject


class DCConejoChico(QObject):

    def __init__(self, client: Client, user_name: str, level: int = 1):
        super().__init__()
        self.game = GameEngine(user_name, level)
        self.window = FullWindow(level)
        self.client = client

    def client_signals(self):
        self.game.change_score.connect(self.client.send)

    def key_signals(self):
        self.window.game_window.key_signal.connect(
            self.game.rabbit.get_direction)
        self.window.game_window.key_signal.connect(self.game.grab_item)

        self.window.game_window.mouse_signal.connect(self.game.use_item)

        self.window.game_window.kill_adds.connect(self.game.k_i_l)
        self.window.game_window.infinity.connect(self.game.i_n_f)

    def placement_signals(self):
        self.game.spawn_rabbit.connect(self.window.game_window.place_rabbit)

        self.game.spawn_wolf.connect(self.window.game_window.place_wolf)

        self.game.spawn_cannon.connect(self.window.game_window.place_cannon)

        self.game.place_item.connect(self.window.game_window.place_item)

    def movement_signals(self):
        self.game.rabbit.animate.connect(self.window.game_window.rabbit._move)

        for wolf in self.game.wolves.values():
            wolf.animate.connect(
                self.window.game_window.wolf_widgets[wolf._id]._move)

    def game_event_signals(self):
        self.game.rabbit.position.connect(self.game.update_positions)
        self.game.rabbit.wall_colision.connect(
            self.window.game_window.rabbit.wall_colision)
        self.game.bunny_hit.connect(self.window.game_window.rabbit.bunny_hit)

        for wolf in self.game.wolves.values():
            wolf.position.connect(self.game.update_positions)

        for cannon in self.game.cannons.values():
            cannon.spawn_carrot.connect(self.game.instance_carrot)
            cannon.spawn_carrot.connect(self.window.game_window.spawn_carrot)

        self.game.remove_item.connect(self.window.game_window.remove_item)

        self.game.place_fire_zone.connect(
            self.window.game_window.place_fire_zone)
        self.game.place_ice_zone.connect(
            self.window.game_window.place_ice_zone)

        self.game.remove_fire_zone.connect(
            self.window.game_window.remove_fire_zone)
        self.game.remove_ice_zone.connect(
            self.window.game_window.remove_ice_zone)

        self.game.remove_wolf.connect(self.window.game_window.remove_wolf)
        self.game.slow_wolf.connect(self.window.game_window.slow_wolf)
        self.game.normalize_wolves.connect(
            self.window.game_window.normalize_wolves)

        self.game.add_to_inventory.connect(self.window.left_menu.add_item)

        self.window.left_menu.item_list.itemClicked.connect(
            self.game.select_item)
        self.window.left_menu.item_list.itemClicked.connect(
            self.window.game_window.setFocus)
        self.window.left_menu.deselect_button.clicked.connect(
            self.game.select_item)
        self.window.left_menu.deselect_button.clicked.connect(
            self.window.game_window.setFocus)
        self.game.placement_error.connect(self.window.error_sound.play)

        self.game.remove_from_inventory.connect(
            self.window.left_menu.remove_item)

        self.window.game_window.pause_signal.connect(self.game.pause)

        self.window.left_menu.pause_button.clicked.connect(self.game.pause)
        self.window.left_menu.pause_button.clicked.connect(
            self.window.game_window.pause)
        self.window.left_menu.pause_button.clicked.connect(
            self.window.game_window.setFocus)

        self.game.tick.connect(self.window.left_menu.update_time)
        self.game.score.connect(self.window.left_menu.update_score)

        self.game.exit_animation.connect(
            self.window.game_window.rabbit.exit_animation)

        self.window.game_window.rabbit.exited.connect(
            self.window.left_menu.switch_button)

        self.window.left_menu.next_level_button.clicked.connect(
            self.game.prep_next_level)

        self.game.next_level.connect(self.next_level)

        self.window.right_menu.heart_list.itemClicked.connect(
            self.window.game_window.setFocus)
        self.game.add_heart.connect(self.window.right_menu.add_heart)
        self.game.remove_heart.connect(self.window.right_menu.remove_heart)
        self.window.game_window.infinity.connect(
            self.window.right_menu.infinity_mode)

        self.game.game_over.connect(self.window.game_over_popup)

    def start(self):
        self.client_signals()

        self.placement_signals()
        self.game.instance_sprites()

        self.key_signals()
        self.movement_signals()
        self.game_event_signals()

        self.window.left_menu.item_list.clear()
        self.game.add_items_to_inventory()

        self.window.right_menu.heart_list.clear()
        self.game.add_hearts()
        self.window.right_menu.raise_()

        self.window.show()

    def next_level(self, user_name: str, level: int, hp: int, items: list[str]):
        if level == 4:
            self.window.victory_popup()
            return

        self.game = GameEngine(
            user_name, level, rabbit_hp=hp, past_items=items)
        self.window.game_window.setFocus()
        self.window.change_game_widget(level)
        self.window.left_menu.switch_button()
        self.start()


if __name__ == "__main__":
    pass
