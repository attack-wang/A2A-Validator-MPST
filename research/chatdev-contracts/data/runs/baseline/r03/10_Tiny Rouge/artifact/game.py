'''
game.py
Core game logic for the roguelike. The Game class owns the current level
(grid, door, monsters, chests), the player and the HUD message log. It
resolves W/A/S/D movement: walking into walls is blocked, stepping on a
monster triggers combat (monster HP is subtracted from player HP), stepping
on a chest restores 20-30 HP, and stepping on the door advances to the next
level while keeping the player's HP.
'''
import config
import map_generator
from entities import Player
class Game:
    def __init__(self):
        self.level = 1
        self.messages = []          # log lines shown in the HUD
        self.last_monster = None    # stats of the last encountered monster
        self.game_over = False
        self.player = None
        self.load_level(1)
    # ------------------------------------------------------------------
    # Level handling
    # ------------------------------------------------------------------
    def load_level(self, level):
        '''Generate a new level. The player object (and therefore its HP)
        is preserved across levels.'''
        data = map_generator.generate_level(level)
        self.grid = data["grid"]
        self.door = data["door"]
        self.monsters = data["monsters"]
        self.chests = data["chests"]
        sx, sy = data["start"]
        if self.player is None:
            self.player = Player(sx, sy)
        else:
            self.player.x = sx
            self.player.y = sy
        self.last_monster = None
        self.add_message(f"-- Floor {level} -- Reach the door. (R: restart)")
    def add_message(self, text):
        self.messages.append(text)
        if len(self.messages) > 4:
            self.messages.pop(0)
    # ------------------------------------------------------------------
    # Movement and interaction
    # ------------------------------------------------------------------
    def handle_move(self, dx, dy):
        '''Process one W/A/S/D step. Ignores input when the game is over.'''
        if self.game_over or self.player is None:
            return
        nx, ny = self.player.x + dx, self.player.y + dy
        if not self._walkable(nx, ny):
            return  # walls block movement
        self.player.move(dx, dy)
        self._resolve_tile(nx, ny)
        if not self.player.alive:
            self.game_over = True
            self.add_message("You died! Press R to restart.")
    def _walkable(self, x, y):
        '''Floor tiles and the door tile can be entered; walls cannot.'''
        if not (0 <= x < config.GRID_WIDTH and 0 <= y < config.GRID_HEIGHT):
            return False
        tile = self.grid[y][x]
        return tile in (config.TILE_FLOOR, config.TILE_DOOR)
    def _resolve_tile(self, x, y):
        '''Combat, chest pickup and door logic for the tile the player
        just stepped onto.'''
        # Monster combat: subtract the monster's HP from the player's HP.
        monster = next((m for m in self.monsters if m.pos == (x, y)), None)
        if monster is not None:
            self.last_monster = monster
            self.player.take_damage(monster.hp)
            self.monsters.remove(monster)
            self.add_message(f"Fought {monster.stats_text()} -> -{monster.hp} HP")
            if not self.player.alive:
                return
        # Treasure chest: restore 20-30 HP.
        chest = next((c for c in self.chests if c.pos == (x, y)), None)
        if chest is not None:
            heal = chest.open()
            self.player.heal(heal)
            self.chests.remove(chest)
            self.add_message(f"Opened a chest: +{heal} HP (HP {self.player.hp})")
        # Door: advance to the next level, HP persists.
        if self.door.pos == (x, y):
            self.level += 1
            self.add_message("You found the door! Descending...")
            self.load_level(self.level)
    # ------------------------------------------------------------------
    # Restart
    # ------------------------------------------------------------------
    def restart(self):
        '''Start a brand new run from floor 1 with full HP.'''
        self.level = 1
        self.messages = []
        self.last_monster = None
        self.game_over = False
        self.player = None
        self.load_level(1)