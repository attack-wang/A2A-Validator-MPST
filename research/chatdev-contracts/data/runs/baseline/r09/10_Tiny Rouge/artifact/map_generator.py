'''Procedural generation of the fixed 80x80 tower floor with a guaranteed path.'''
import random
from settings import ...
from pathfinding import has_path, bfs_reachable
class FloorMap:
    """Holds the tile grid plus entities placed on one tower floor."""
    def __init__(self, grid, start, door, monsters, chests):
        ...
class MapGenerator:
    def generate(self, level):
        for attempt in range(MAX_ATTEMPTS):
            grid, start, door = self._carve(level)
            monsters, chests = self._populate(grid, start, door, level)
            if has_path(...): return FloorMap(...)
        # fallback: straight corridor carve (guaranteed)