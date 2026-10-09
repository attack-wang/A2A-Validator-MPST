'''
level.py
Procedural generation of one 80x80 tower floor.
Rooms are carved into a solid wall grid and connected with L-shaped
corridors.  A BFS check guarantees there is always at least one walkable
path from the starting position to the door before the floor is accepted;
monsters are never placed on that critical path.
'''
from collections import deque
from settings import (
    GRID_WIDTH, GRID_HEIGHT,
    TILE_WALL, TILE_FLOOR, TILE_DOOR,
    ROOMS_TARGET, ROOM_MIN_SIZE, ROOM_MAX_SIZE, ROOM_PLACEMENT_ATTEMPTS,
    EXTRA_CORRIDORS, MAX_GENERATION_ATTEMPTS,
    MONSTER_BASE_COUNT, MONSTER_PER_LEVEL, MONSTER_HARD_CAP,
    CHEST_BASE_COUNT, CHEST_PER_LEVEL, CHEST_HARD_CAP,
    MONSTER_TEMPLATES,
)
from entities import Monster
class GenerationError(Exception):
    """Raised when one generation attempt fails and must be retried."""
class Level:
    """One 80x80 tower floor: rooms carved into walls, guaranteed start->door path."""
    def __init__(self, level_number, rng):
        self.number = level_number
        self.rng = rng
        self.grid = []
        self.rooms = []
        self.monsters = {}      # (x, y) -> Monster
        self.chests = set()     # {(x, y)}
        self.start = None       # (x, y)
        self.door = None        # (x, y)
        self._generate()
    # ------------------------------------------------------------------
    # Generation pipeline
    # ------------------------------------------------------------------
    def _generate(self):
        """Build a valid floor, retrying until a start->door path is guaranteed."""
        for _ in range(MAX_GENERATION_ATTEMPTS):
            try:
                self._carve_map()
                self._place_start_and_door()
                if not self._verify_connectivity():
                    continue
                path = self._bfs_path(self.start, self.door)
                self._place_monsters_and_chests(path)
                return
            except GenerationError:
                continue
        self._fallback_floor()
    def _carve_map(self):
        """Fill the grid with walls, then carve rooms and connect them."""
        self.grid = [[TILE_WALL for _ in range(GRID_WIDTH)]
                     for _ in range(GRID_HEIGHT)]
        self.rooms = []
        for _ in range(ROOM_PLACEMENT_ATTEMPTS):
            if len(self.rooms) >= ROOMS_TARGET:
                break
            w = self.rng.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = self.rng.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            x = self.rng.randint(1, GRID_WIDTH - w - 2)
            y = self.rng.randint(1, GRID_HEIGHT - h - 2)
            room = (x, y, w, h)
            if any(self._rooms_overlap(room, other) for other in self.rooms):
                continue
            self._carve_room(room)
            self.rooms.append(room)
        if len(self.rooms) < 2:
            raise GenerationError("could not place enough rooms")
        for i in range(1, len(self.rooms)):
            self._carve_corridor(self._room_center(self.rooms[i - 1]),
                                 self._room_center(self.rooms[i]))
        for _ in range(EXTRA_CORRIDORS):
            a = self._room_center(self.rng.choice(self.rooms))
            b = self._room_center(self.rng.choice(self.rooms))
            self._carve_corridor(a, b)
    @staticmethod
    def _rooms_overlap(a, b):
        """True when two rooms (with a 1-tile gap) would touch or overlap."""
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return (ax - 1 < bx + bw and bx - 1 < ax + aw and
                ay - 1 < by + bh and by - 1 < ay + ah)
    def _carve_room(self, room):
        x, y, w, h = room
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.grid[yy][xx] = TILE_FLOOR
    @staticmethod
    def _room_center(room):
        x, y, w, h = room
        return (x + w // 2, y + h // 2)
    def _carve_corridor(self, p1, p2):
        """Carve an L-shaped corridor between two points (random bend order)."""
        x1, y1 = p1
        x2, y2 = p2
        if self.rng.random() < 0.5:
            self._carve_horizontal(x1, x2, y1)
            self._carve_vertical(y1, y2, x2)
        else:
            self._carve_vertical(y1, y2, x1)
            self._carve_horizontal(x1, x2, y2)
    def _carve_horizontal(self, x1, x2, y):
        y = max(1, min(GRID_HEIGHT - 2, y))
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.grid[y][x] = TILE_FLOOR
    def _carve_vertical(self, y1, y2, x):
        x = max(1, min(GRID_WIDTH - 2, x))
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.grid[y][x] = TILE_FLOOR
    def _place_start_and_door(self):
        start = self._room_center(self.rooms[0])
        door = self._room_center(self.rooms[-1])
        if start == door:
            raise GenerationError("start and door coincide")
        self.start = start
        self.door = door
        self.grid[start[1]][start[0]] = TILE_FLOOR
        self.grid[door[1]][door[0]] = TILE_DOOR
    def _verify_connectivity(self):
        """Guarantee at least one walkable path from start to door."""
        return self._bfs_path(self.start, self.door) is not None
    def _bfs_path(self, src, dst):
        """BFS over walkable tiles; returns the path as a list or None."""
        if src == dst:
            return [src]
        visited = {src}
        came_from = {}
        queue = deque([src])
        while queue:
            cx, cy = queue.popleft()
            for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                if (nx, ny) in visited or not self.in_bounds(nx, ny):
                    continue
                if self.grid[ny][nx] == TILE_WALL:
                    continue
                visited.add((nx, ny))
                came_from[(nx, ny)] = (cx, cy)
                if (nx, ny) == dst:
                    path = [(nx, ny)]
                    while path[-1] != src:
                        path.append(came_from[path[-1]])
                    path.reverse()
                    return path
                queue.append((nx, ny))
        return None
    def _place_monsters_and_chests(self, path):
        """Populate the floor; monsters never sit on the guaranteed safe path."""
        critical_path = set(path)
        walkable = [(x, y) for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH)
                    if self.grid[y][x] == TILE_FLOOR
                    and (x, y) != self.start and (x, y) != self.door]
        self.rng.shuffle(walkable)
        monster_pool = [tile for tile in walkable if tile not in critical_path]
        monster_count = min(MONSTER_HARD_CAP,
                            MONSTER_BASE_COUNT + MONSTER_PER_LEVEL * (self.number - 1),
                            len(monster_pool))
        max_template = min(len(MONSTER_TEMPLATES) - 1, self.number // 2)
        for _ in range(monster_count):
            x, y = monster_pool.pop()
            name, base_hp = MONSTER_TEMPLATES[self.rng.randint(0, max_template)]
            hp = base_hp + (self.number - 1) * 2
            self.monsters[(x, y)] = Monster(name, hp, x, y)
        chest_pool = [tile for tile in walkable if tile not in self.monsters]
        chest_count = min(CHEST_HARD_CAP,
                          CHEST_BASE_COUNT + CHEST_PER_LEVEL * (self.number - 1),
                          len(chest_pool))
        for _ in range(chest_count):
            x, y = chest_pool.pop()
            self.chests.add((x, y))
    def _fallback_floor(self):
        """Last-resort floor: one big open room, so a path always exists."""
        self.grid = [[TILE_FLOOR for _ in range(GRID_WIDTH)]
                     for _ in range(GRID_HEIGHT)]
        for x in range(GRID_WIDTH):
            self.grid[0][x] = TILE_WALL
            self.grid[GRID_HEIGHT - 1][x] = TILE_WALL
        for y in range(GRID_HEIGHT):
            self.grid[y][0] = TILE_WALL
            self.grid[y][GRID_WIDTH - 1] = TILE_WALL
        self.rooms = [(2, 2, GRID_WIDTH - 4, GRID_HEIGHT - 4)]
        self.start = (2, 2)
        self.door = (GRID_WIDTH - 3, GRID_HEIGHT - 3)
        self.grid[self.door[1]][self.door[0]] = TILE_DOOR
        self._place_monsters_and_chests(self._bfs_path(self.start, self.door))
    # ------------------------------------------------------------------
    # Queries / mutations used by the game rules
    # ------------------------------------------------------------------
    def in_bounds(self, x, y):
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT
    def is_wall(self, x, y):
        return not self.in_bounds(x, y) or self.grid[y][x] == TILE_WALL
    def is_door(self, x, y):
        return self.in_bounds(x, y) and self.grid[y][x] == TILE_DOOR
    def monster_at(self, x, y):
        return self.monsters.get((x, y))
    def chest_at(self, x, y):
        return (x, y) in self.chests
    def remove_monster(self, x, y):
        self.monsters.pop((x, y), None)
    def remove_chest(self, x, y):
        self.chests.discard((x, y))