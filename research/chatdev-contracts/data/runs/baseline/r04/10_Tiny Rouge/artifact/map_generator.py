'''Procedural generation of the 80x80 tower floors.
Guarantees connectivity: a maze is carved with a recursive backtracker
(every floor tile is reachable), extra loops and rooms are added, and the
door is placed on the farthest tile found by BFS from the start, so there
is always at least one valid path from start to door.
'''
import random
from collections import deque
from settings import (GRID_WIDTH, GRID_HEIGHT, TILE_WALL, TILE_FLOOR,
                      TILE_DOOR, MONSTERS_BASE_COUNT, MONSTERS_PER_LEVEL,
                      MONSTERS_MAX_COUNT, CHESTS_BASE_COUNT, CHESTS_MAX_COUNT)
from entities import Monster, Chest
class MapGenerator:
    '''Builds one tower floor: maze + rooms + door + monsters + chests.'''
    def __init__(self, level, width=GRID_WIDTH, height=GRID_HEIGHT, seed=None):
        self.level = level
        self.width = width
        self.height = height
        self.rng = random.Random(seed)
    # ------------------------------------------------------------------
    def generate(self):
        self.grid = [[TILE_WALL] * self.width for _ in range(self.height)]
        self._carve_maze()
        self._braid_maze(0.6)
        self._carve_rooms(self.rng.randint(5, 9))
        start = (1, 1)
        dist = self._bfs_distances(start)
        door = self._pick_door(dist)
        self.grid[door[1]][door[0]] = TILE_DOOR
        monsters, chests = self._place_entities(start, door, dist)
        return {
            "grid": self.grid,
            "start": start,
            "door": door,
            "monsters": monsters,
            "chests": chests,
        }
    # ------------------------------------------------------------------
    def _carve_maze(self):
        '''Iterative recursive-backtracker maze on odd coordinates.'''
        stack = [(1, 1)]
        visited = {(1, 1)}
        self.grid[1][1] = TILE_FLOOR
        dirs = ((0, -2), (0, 2), (-2, 0), (2, 0))
        while stack:
            x, y = stack[-1]
            neighbors = []
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if (1 <= nx <= self.width - 2 and 1 <= ny <= self.height - 2
                        and (nx, ny) not in visited):
                    neighbors.append((nx, ny))
            if neighbors:
                nx, ny = self.rng.choice(neighbors)
                self.grid[(y + ny) // 2][(x + nx) // 2] = TILE_FLOOR
                self.grid[ny][nx] = TILE_FLOOR
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()
    def _braid_maze(self, p):
        '''Knock out one wall per dead end (probability p) to add loops.'''
        dirs = ((0, -1), (0, 1), (-1, 0), (1, 0))
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y][x] != TILE_FLOOR:
                    continue
                open_dirs = [(dx, dy) for dx, dy in dirs
                             if self.grid[y + dy][x + dx] == TILE_FLOOR]
                if len(open_dirs) <= 1 and self.rng.random() < p:
                    walls = [(dx, dy) for dx, dy in dirs
                             if self.grid[y + dy][x + dx] == TILE_WALL]
                    if not walls:
                        continue
                    dx, dy = self.rng.choice(walls)
                    wx, wy = x + dx, y + dy
                    fx, fy = x + 2 * dx, y + 2 * dy
                    # Only open into a floor cell two steps away so the
                    # border wall is never breached.
                    if (1 <= fx <= self.width - 2 and 1 <= fy <= self.height - 2
                            and self.grid[fy][fx] == TILE_FLOOR):
                        self.grid[wy][wx] = TILE_FLOOR
    def _carve_rooms(self, count):
        '''Carve random rectangular rooms (only adds floor -> stays connected).'''
        for _ in range(count):
            w = self.rng.randint(3, 9)
            h = self.rng.randint(3, 9)
            x0 = self.rng.randint(1, self.width - 2 - (w - 1))
            y0 = self.rng.randint(1, self.height - 2 - (h - 1))
            for y in range(y0, y0 + h):
                for x in range(x0, x0 + w):
                    self.grid[y][x] = TILE_FLOOR
    def _bfs_distances(self, start):
        '''BFS over floor tiles; returns {(x, y): distance}.'''
        dist = {start: 0}
        queue = deque([start])
        dirs = ((0, -1), (0, 1), (-1, 0), (1, 0))
        while queue:
            x, y = queue.popleft()
            d = dist[(x, y)]
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height
                        and self.grid[ny][nx] == TILE_FLOOR
                        and (nx, ny) not in dist):
                    dist[(nx, ny)] = d + 1
                    queue.append((nx, ny))
        return dist
    def _pick_door(self, dist):
        '''Place the door on the farthest reachable floor tile from start.'''
        farthest = max(dist.items(), key=lambda item: item[1])
        candidates = [pos for pos, d in dist.items() if d == farthest[1]]
        door = self.rng.choice(candidates)
        return door
    def _place_entities(self, start, door, dist):
        '''Scatter monsters and chests on reachable floor tiles.'''
        sx, sy = start
        forbidden = {start, door}
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                forbidden.add((sx + dx, sy + dy))
        floor_tiles = [pos for pos in dist
                       if pos not in forbidden]
        self.rng.shuffle(floor_tiles)
        monster_count = min(MONSTERS_BASE_COUNT + MONSTERS_PER_LEVEL * (self.level - 1),
                            MONSTERS_MAX_COUNT, len(floor_tiles))
        monsters = {}
        for pos in floor_tiles[:monster_count]:
            monsters[pos] = Monster.spawn(pos[0], pos[1], self.level, self.rng)
        remaining = floor_tiles[monster_count:]
        chest_count = min(CHESTS_BASE_COUNT + self.level // 2,
                          CHESTS_MAX_COUNT, len(remaining))
        chests = {}
        for pos in remaining[:chest_count]:
            chests[pos] = Chest.spawn(pos[0], pos[1], self.rng)
        return monsters, chests