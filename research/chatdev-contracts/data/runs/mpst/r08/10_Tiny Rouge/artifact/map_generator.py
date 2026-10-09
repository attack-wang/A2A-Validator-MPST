'''
map_generator.py
Procedural generation of 80x80 levels with a guaranteed start→door path.
'''
import random
from collections import deque
import settings
from entities import Monster, TreasureChest
from level import Level
class MapGenerator:
    """Generates dungeon levels: maze carving, room carving, entity placement."""
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
    def generate(self, level_number):
        """Generate one complete level. Retries (iteratively) until a valid path exists."""
        start = (settings.PLAYER_START_X, settings.PLAYER_START_Y)
        door = (settings.GRID_WIDTH - 3, settings.GRID_HEIGHT - 3)  # (77, 77) — odd cell, always reachable by the carver
        while True:
            grid = self._carve_maze()
            self._braid_dead_ends(grid)
            self._carve_rooms(grid)
            # ensure start and door tiles are floor
            grid[start[1]][start[0]] = settings.TILE_FLOOR
            grid[door[1]][door[0]] = settings.TILE_FLOOR
            if self._path_exists(grid, start, door):
                break  # valid layout found
        monsters, chests = self._populate(grid, level_number, start, door)
        return Level(level_number, grid, start, door, monsters, chests)