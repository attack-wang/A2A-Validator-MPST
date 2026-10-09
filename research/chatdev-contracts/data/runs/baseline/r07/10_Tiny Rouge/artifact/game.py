'''
game.py
Core game state and turn logic: player movement, monster combat,
treasure chests, and descending to the next level.
'''
import pygame
from entities import Player
from map_generator import generate_map
# Incremented every time a new map is generated; the renderer uses it as a
# cache key so the static map layer is rebuilt only when the floor changes.
_map_version_counter = 0
class Game:
    '''Holds the current level, player, messages and game-over state.'''
    def __init__(self):
        self.restart()
    def restart(self):
        '''Start a brand-new run at level 1 with a fresh player.'''
        self.level = 1
        self.map_version = 0
        self.encountered_monster = None
        self.messages = []
        self.game_over = False
        self.player = None
        self._new_level(1)
        self.add_message("New game! Reach the door.")
    def _new_level(self, level):
        '''Generate floor `level` and place the player at its start position.'''
        global _map_version_counter
        _map_version_counter += 1
        self.map_version = _map_version_counter
        self.level = level
        self.game_map = generate_map(level)
        start = self.game_map.start
        if self.player is None:
            self.player = Player(start[0], start[1])
        else:
            self.player.x, self.player.y = start
        self.encountered_monster = None
    def add_message(self, text):
        '''Append a message to the HUD log (keeps the last 6 entries).'''
        self.messages.append(text)
        if len(self.messages) > 6:
            self.messages.pop(0)
    def handle_key(self, key):
        '''Translate a pygame key event into a game action.'''
        if self.game_over:
            if key == pygame.K_r:
                self.restart()
            return
        moves = {
            pygame.K_w: (0, -1),
            pygame.K_a: (-1, 0),
            pygame.K_s: (0, 1),
            pygame.K_d: (1, 0),
        }
        if key in moves:
            dx, dy = moves[key]
            self.try_move(dx, dy)
    def try_move(self, dx, dy):
        '''Attempt to move the player one tile by (dx, dy).
        Walls block movement; monsters trigger combat; chests heal;
        the door descends to the next level.'''
        nx = self.player.x + dx
        ny = self.player.y + dy
        if not self.game_map.in_bounds(nx, ny):
            return
        if self.game_map.is_wall(nx, ny):
            self.add_message("A wall blocks your way.")
            return
        monster = self.game_map.monster_at(nx, ny)
        if monster is not None:
            self.fight_monster(monster)
            if not self.player.alive:
                return
            # Player survives: step onto the defeated monster's tile.
        chest = self.game_map.chest_at(nx, ny)
        if chest is not None:
            self.open_chest(chest)
        door = self.game_map.door
        if nx == door.x and ny == door.y:
            self.descend()
            return
        self.player.x, self.player.y = nx, ny
    def fight_monster(self, monster):
        '''Tower-of-the-Sorcerer style combat: the monster's HP is subtracted
        from the player's HP and the monster is slain (removed from the map).
        If the player's HP reaches 0 the run ends.'''
        self.encountered_monster = monster  # stats stay visible in the UI
        damage = monster.hp
        died = self.player.take_damage(damage)
        self.game_map.monsters.remove(monster)
        self.add_message(f"{monster.name} slain! -{damage} HP")
        if died:
            self.game_over = True
            self.add_message("You died... Press R to restart.")
    def open_chest(self, chest):
        '''Touching a treasure chest restores a random 20-30 HP (rolled when
        the chest was created) and removes the chest from the map.'''
        healed = self.player.heal(chest.heal_amount)
        self.game_map.chests.remove(chest)
        self.add_message(f"Treasure chest! Restored {healed} HP.")
    def descend(self):
        '''The player reached the door: build the next floor.'''
        self._new_level(self.level + 1)
        self.add_message(f"You descended to level {self.level}!")