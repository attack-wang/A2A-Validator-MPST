import random
from collections import deque
import config
from entities import Monster, TreasureChest
class GameMap:
    def __init__(self, grid, start, door, monsters, chests):
        self.grid = grid
        self.start = start
        self.door = door
        self.monsters = monsters
        self.chests = chests
    def in_bounds(self, x, y):
        return 0 <= x < config.GRID_WIDTH and 0 <= y < config.GRID_HEIGHT
    def tile_at(self, x, y):
        return self.grid[y][x]
    def is_floor(self, x, y):
        return self.in_bounds(x, y) and self.grid[y][x] != config.TILE_WALL
    def monster_at(self, x, y):
        for m in self.monsters:
            if m.x == x and m.y == y:
                return m
        return None
    def chest_at(self, x, y):
        for c in self.chests:
            if c.x == x and c.y == y:
                return c
        return None