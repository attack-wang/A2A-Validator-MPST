'''
map_generator.py
...
'''
import random
from collections import deque
import game_constants as C
from entities import Monster, TreasureChest, Door
class GameMap:
    def __init__(self, grid, start, door, monsters, chests):
        self.grid = grid
        self.start = start
        self.door = door          # Door instance (has .pos)
        self.monsters = monsters
        self.chests = chests
    def in_bounds(self, x, y):
        return 0 <= x < C.GRID_SIZE and 0 <= y < C.GRID_SIZE
    def is_floor(self, x, y):
        return self.in_bounds(x, y) and self.grid[y][x] == C.TILE_FLOOR
    def is_wall(self, x, y):
        return self.in_bounds(x, y) and self.grid[y][x] == C.TILE_WALL
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
    def remove_monster(self, monster):
        if monster in self.monsters:
            self.monsters.remove(monster)
    def remove_chest(self, chest):
        if chest in self.chests:
            self.chests.remove(chest)
def _carve_maze(grid, rng):
    """Iterative recursive-backtracker maze on odd coordinates."""
    height = len(grid)
    width = len(grid[0])
    grid[1][1] = C.TILE_FLOOR
    stack = [(1, 1)]
    visited = {(1, 1)}
    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in ((0, -2), (0, 2), (-2, 0), (2, 0)):
            nx, ny = x + dx, y + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and (nx, ny) not in visited:
                neighbors.append((nx, ny, dx, dy))
        if neighbors:
            nx, ny, dx, dy = rng.choice(neighbors)
            grid[y + dy // 2][x + dx // 2] = C.TILE_FLOOR
            grid[ny][nx] = C.TILE_FLOOR
            visited.add((nx, ny))
            stack.append((nx, ny))
        else:
            stack.pop()
def _carve_rooms(grid, rng):
    """Carve a few small rectangular rooms to open up the maze."""
    height = len(grid)
    width = len(grid[0])
    for _ in range(C.ROOMS_TO_CARVE):
        room_w = rng.randint(3, 9)
        room_h = rng.randint(3, 9)
        x0 = rng.randint(1, width - 2 - room_w)
        y0 = rng.randint(1, height - 2 - room_h)
        for y in range(y0, y0 + room_h):
            for x in range(x0, x0 + room_w):
                grid[y][x] = C.TILE_FLOOR
def _braid_walls(grid, rng):
    """Randomly open interior walls to create loops (multiple routes)."""
    height = len(grid)
    width = len(grid[0])
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if grid[y][x] == C.TILE_WALL and rng.random() < C.BRAID_CHANCE:
                # only open walls that separate two floor tiles (horizontal or vertical)
                if (grid[y][x - 1] == C.TILE_FLOOR and grid[y][x + 1] == C.TILE_FLOOR) or \
                   (grid[y - 1][x] == C.TILE_FLOOR and grid[y + 1][x] == C.TILE_FLOOR):
                    grid[y][x] = C.TILE_FLOOR
def _carve_layout(rng):
    grid = [[C.TILE_WALL for _ in range(C.GRID_SIZE)] for _ in range(C.GRID_SIZE)]
    _carve_maze(grid, rng)
    _carve_rooms(grid, rng)
    _braid_walls(grid, rng)
    # keep the outer border solid wall
    for i in range(C.GRID_SIZE):
        grid[0][i] = C.TILE_WALL
        grid[C.GRID_SIZE - 1][i] = C.TILE_WALL
        grid[i][0] = C.TILE_WALL
        grid[i][C.GRID_SIZE - 1] = C.TILE_WALL
    return grid