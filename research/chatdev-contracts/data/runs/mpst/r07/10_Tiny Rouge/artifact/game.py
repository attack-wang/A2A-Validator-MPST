'''
game.py
Core rules and state of the roguelike: the Game class.
Responsibilities:
- build a level via map_generator and place monsters/chests/door
- validate W/A/S/D movement against walls and grid borders
- bump-to-fight combat (player loses HP equal to monster HP)
- treasure chests that heal 20-30 HP
- stepping on the door advances to the next, harder level
- a short message log that the console UI renders
Pure standard library only - no pygame required.
'''
import random
from config import (
    GRID_SIZE, TILE_FLOOR, TILE_WALL, TILE_DOOR,
    MONSTER_TEMPLATES, MONSTER_COUNT_BASE, MONSTER_COUNT_PER_LEVEL,
    MONSTER_HP_LEVEL_SCALE, CHEST_COUNT_BASE, CHEST_COUNT_PER_LEVEL,
)
from entities import Player, Monster, TreasureChest, Door
from map_generator import generate_level
# log message kinds
LOG_INFO = "info"
LOG_GOOD = "good"
LOG_BAD = "bad"
LOG_EVENT = "event"
class Game:
    def __init__(self):
        self.rng = random.Random()
        self.state = "playing"          # "playing" or "game_over"
        self.level = 1
        self.log = []                   # list of (text, kind)
        self.last_monster = None        # last monster the player met
        self.map_version = 0            # bumped whenever the map changes
        self.restart()
    # ------------------------------------------------------------------
    # Level setup
    # ------------------------------------------------------------------
    def restart(self):
        '''Reset the whole run back to level 1 with fresh HP.'''
        self.level = 1
        self.log = []
        self.last_monster = None
        self.state = "playing"
        self._start_level(1, fresh_player=True)
    def _start_level(self, level, fresh_player=False):
        '''Generate level `level` and populate it with monsters & chests.'''
        self.level = level
        grid, start, door, safe_path = generate_level(level, self.rng)
        self.grid = grid
        self.safe_path = set(safe_path)
        self.door = Door(door[0], door[1])
        if fresh_player or not hasattr(self, "player"):
            self.player = Player(start[0], start[1])
        else:
            self.player.move_to(start[0], start[1])
        self.monsters = []
        self.chests = []
        self._spawn_monsters()
        self._spawn_chests()
        self.map_version += 1
        self.add_message("-- Level {} --".format(level), LOG_EVENT)
        self.add_message("Reach the golden door 'D'!", LOG_INFO)
    def _spawn_monsters(self):
        count = MONSTER_COUNT_BASE + MONSTER_COUNT_PER_LEVEL * (self.level - 1)
        free = self._free_spawn_tiles()
        self.rng.shuffle(free)
        for i in range(min(count, len(free))):
            x, y = free[i]
            template = self.rng.choice(MONSTER_TEMPLATES)
            hp = template["hp"] + MONSTER_HP_LEVEL_SCALE * (self.level - 1)
            self.monsters.append(Monster(x, y, template["name"], hp, template["symbol"]))
    def _spawn_chests(self):
        count = CHEST_COUNT_BASE + CHEST_COUNT_PER_LEVEL * (self.level - 1)
        free = self._free_spawn_tiles()
        self.rng.shuffle(free)
        taken = {(m.x, m.y) for m in self.monsters}
        placed = 0
        for x, y in free:
            if (x, y) in taken:
                continue
            self.chests.append(TreasureChest(x, y))
            placed += 1
            if placed >= count:
                break
    def _free_spawn_tiles(self):
        '''
        Floor tiles that are NOT the start tile, NOT the door tile and NOT
        on the guaranteed safe path. This keeps at least one valid route
        from start to door permanently open (customer requirement).
        '''
        occupied = self.safe_path | {(self.player.x, self.player.y), self.door.pos}
        free = []
        for y in range(1, GRID_SIZE - 1):
            for x in range(1, GRID_SIZE - 1):
                if self.grid[y][x] == TILE_FLOOR and (x, y) not in occupied:
                    free.append((x, y))
        return free
    # ------------------------------------------------------------------
    # Messages
    # ------------------------------------------------------------------
    def add_message(self, text, kind=LOG_INFO):
        self.log.append((text, kind))
        if len(self.log) > 8:
            self.log.pop(0)
    # ------------------------------------------------------------------
    # Movement & interactions
    # ------------------------------------------------------------------
    def handle_move(self, dx, dy):
        '''Try to move the player one tile. Called for W/A/S/D input.'''
        if self.state != "playing":
            return
        nx = self.player.x + dx
        ny = self.player.y + dy
        if not (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE):
            return
        if self.grid[ny][nx] == TILE_WALL:
            self.add_message("A wall blocks your way.", LOG_INFO)
            return
        monster = self._monster_at(nx, ny)
        if monster is not None:
            self._fight_monster(monster)
        else:
            self.player.move_to(nx, ny)
            self._pickup_chest_at(nx, ny)
            if (nx, ny) == self.door.pos:
                self._next_level()
    def _monster_at(self, x, y):
        for m in self.monsters:
            if m.x == x and m.y == y:
                return m
        return None
    def _chest_at(self, x, y):
        for c in self.chests:
            if c.x == x and c.y == y:
                return c
        return None
    def _fight_monster(self, monster):
        '''Bump combat: player loses HP equal to the monster's HP.'''
        self.last_monster = monster
        dealt = self.player.take_damage(monster.hp)
        self.monsters.remove(monster)
        self.add_message(
            "Fought {}! -{} HP".format(monster.describe(), dealt), LOG_BAD)
        if not self.player.is_alive():
            self.state = "game_over"
            self.add_message("You died... press R to restart.", LOG_BAD)
    def _pickup_chest_at(self, x, y):
        chest = self._chest_at(x, y)
        if chest is not None:
            healed = self.player.heal(chest.heal_amount)
            self.chests.remove(chest)
            self.add_message("Treasure chest! +{} HP".format(healed), LOG_GOOD)
    def _next_level(self):
        self.add_message("Door opened! Descending...", LOG_EVENT)
        self._start_level(self.level + 1)