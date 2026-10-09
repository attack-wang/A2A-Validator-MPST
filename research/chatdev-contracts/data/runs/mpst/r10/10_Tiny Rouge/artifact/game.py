'''
game.py
Core game state and rules: movement, combat, chests, level flow.
'''
import config
from entities import Monster, TreasureChest, Player
from map_generator import MapGenerator
class Game:
    """Central controller tying together the player, the map and the UI."""
    def __init__(self):
        self.level = 1
        self.player = Player(0, 0)          # position set by the map generator
        self.game_map = MapGenerator().generate(self.level, self.player.hp)
        self.player.x, self.player.y = self.game_map.start
        self.messages = []                  # message log for the UI panel
        self.game_over = False
        self.victory = False
        self._log("You enter the tower. Reach the green door!")
    def handle_move(self, direction):
        """Process one W/A/S/D step: ('up', 'left', 'down', 'right')."""
        if self.game_over:
            return
        dx, dy = {'up': (0, -1), 'down': (0, 1),
                  'left': (-1, 0), 'right': (1, 0)}[direction]
        nx, ny = self.player.x + dx, self.player.y + dy
        if not self.game_map.in_bounds(nx, ny) or self.game_map.is_wall(nx, ny):
            self._log("A wall blocks your way.")
            return
        entity = self.game_map.entity_at(nx, ny)
        if isinstance(entity, Monster):
            # Combat: the monster's HP is subtracted from the player's HP.
            self.player.take_damage(entity.damage)
            self.game_map.remove_entity(entity)
            self._log(f"You slew {entity.name} (-{entity.damage} HP).")
            if not self.player.is_alive():
                self.game_over = True
                self._log("You have died. Press R to restart.")
                return
        elif isinstance(entity, TreasureChest):
            healed = self.player.heal(entity.heal_amount)
            self.game_map.remove_entity(entity)
            self._log(f"Chest opened: +{healed} HP.")
        elif self.game_map.is_door(nx, ny):
            self.level += 1
            self.player.heal(config.LEVEL_CLEAR_BONUS)
            self.game_map = MapGenerator().generate(self.level, self.player.hp)
            self.player.x, self.player.y = self.game_map.start
            self._log(f"You descend to floor {self.level}.")
            return
        self.player.move_to(nx, ny)
    def restart(self):
        """Re-initialize the whole game for the 'R' key."""
        self.__init__()
    def _log(self, text):
        self.messages.append(text)
        del self.messages[:-config.MESSAGE_LOG_LENGTH]