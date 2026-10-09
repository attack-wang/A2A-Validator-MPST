'''
Procedural map generation with a guaranteed start-to-door path (BFS validated).
'''
import random
from collections import deque
from constants import (GRID_WIDTH, GRID_HEIGHT, TILE_WALL, TILE_FLOOR, TILE_DOOR,
                       MONSTERS_PER_LEVEL_BASE, MONSTERS_PER_LEVEL_GROWTH,
                       CHESTS_PER_LEVEL_BASE, CHESTS_PER_LEVEL_GROWTH, ROOMS_PER_LEVEL)
from entities import Monster, Chest
from monsters import pick_monster_template
class GameMap:
    """Container for one level: grid, start, door, monsters, chests."""
    def __init__(self, grid, start, door, monsters, chests):
        self.grid = grid
        self.start = start
        self.door = door
        self.monsters = monsters
        self.chests = chests
    def is_wall(self, x, y):
        """Return True if the tile is a wall (out of bounds counts as wall)."""
        if x < 0 or y < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
            return True
        return self.grid[y][x] == TILE_WALL
class MapGenerator:
    """Generates room-and-corridor maps and guarantees a start->door path."""
    def __init__(self, rng_seed=None):
        self.rng = random.Random(rng_seed)
    def generate(self, level):
        """Generate a full level; regenerate until BFS confirms a valid path."""
        while True:
            grid = self._carve_rooms_and_corridors()
            start, door = self._place_start_and_door(grid)
            if self._path_exists(grid, start, door):
                monsters = self._place_monsters(grid, level, start, door)
                chests = self._place_chests(grid, level, start, door)
                return GameMap(grid, start, door, monsters, chests)
    def _carve_rooms_and_corridors(self):
        """Fill grid with walls, then carve random rooms and connect them."""
        grid = [[TILE_WALL for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        rooms = []
        attempts = 0
        while len(rooms) < ROOMS_PER_LEVEL and attempts < 300:
            attempts += 1
            w = self.rng.randint(6, 14)
            h = self.rng.randint(6, 14)
            x = self.rng.randint(1, GRID_WIDTH - w - 2)
            y = self.rng.randint(1, GRID_HEIGHT - h - 2)
            new_room = (x, y, w, h)
            # Reject rooms overlapping existing ones (with 1-tile margin)
            if any(self._rooms_overlap(new_room, other) for other in rooms):
                continue
            rooms.append(new_room)
        # Carve room interiors
        for (rx, ry, rw, rh) in rooms:
            for yy in range(ry, ry + rh):
                for xx in range(rx, rx + rw):
                    grid[yy][xx] = TILE_FLOOR
        # Connect each room to the previous with an L-shaped corridor
        for i in range(1, len(rooms)):
            cx1, cy1 = self._room_center(rooms[i - 1])
            cx2, cy2 = self._room_center(rooms[i])
            self._carve_corridor(grid, cx1, cy1, cx2, cy2)
        return grid
    ...