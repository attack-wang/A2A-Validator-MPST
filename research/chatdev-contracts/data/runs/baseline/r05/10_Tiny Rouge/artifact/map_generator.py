'''
map_generator.py
Generation of the fixed 80x80 tower floor: a maze-based layout that
guarantees at least one walkable path between the start position and
the door.
'''
import random
from collections import deque
import config
class MapGenerator:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
    def generate(self, level):
        grid = self._carve_maze()
        self._braid(grid)
        start = (1, 1)
        door = (config.GRID_SIZE - 3, config.GRID_SIZE - 3)  # (77,77)
        grid[door[1]][door[0]] = config.DOOR
        path = self._bfs_path(grid, start, door)
        # Safety: if somehow no path (should not happen), carve one.
        if path is None:
            path = self._carve_direct_path(grid, start, door)
            ...
        return grid, start, door, set(path)