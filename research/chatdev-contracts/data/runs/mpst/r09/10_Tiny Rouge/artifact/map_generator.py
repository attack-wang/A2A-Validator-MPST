'''
map_generator.py
Procedural generation of the fixed 80x80 level grid with guaranteed
start-to-door connectivity, plus placement of monsters and chests.
'''
import random
from collections import deque
import config
from entities import Monster, TreasureChest, Door
class LevelData:
    """Container for everything that defines one generated level."""
    def __init__(self, grid, start, door, monsters, chests):
        self.grid = grid
        self.start = start
        self.door = door
        self.monsters = monsters
        self.chests = chests
class MapGenerator:
    def __init__(self, rng=None):
        self.rng = rng or random.Random()
    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def generate_level(self, level):
        for attempt in range(config.MAX_GENERATION_ATTEMPTS):
            grid, rooms = self._carve_rooms_and_corridors()
            if not rooms:
                continue
            start = self._room_center(rooms[0])
            door_room = self._farthest_room(grid, start, rooms)
            door_pos = self._pick_floor_in_room(grid, door_room)
            if door_pos is None:
                continue
            if self._has_path(grid, start, door_pos):
                monsters = self._place_monsters(grid, level, start, door_pos)
                chests = self._place_chests(grid, start, door_pos, monsters)
                return LevelData(grid, start, Door(*door_pos), monsters, chests)
        return self._fallback_level(level)
    # ------------------------------------------------------------------ #
    # Room carving / corridors
    # ------------------------------------------------------------------ #
    def _carve_rooms_and_corridors(self):
        grid = [[config.TILE_WALL for _ in range(config.GRID_SIZE)]
                for _ in range(config.GRID_SIZE)]
        rooms = []
        for _ in range(config.MAX_ROOMS * 3):
            if len(rooms) >= config.MAX_ROOMS:
                break
            w = self.rng.randint(config.ROOM_MIN_SIZE, config.ROOM_MAX_SIZE)
            h = self.rng.randint(config.ROOM_MIN_SIZE, config.ROOM_MAX_SIZE)
            x = self.rng.randint(1, config.GRID_SIZE - w - 1)
            y = self.rng.randint(1, config.GRID_SIZE - h - 1)
            new_room = (x, y, w, h)
            if any(self._rooms_overlap(new_room, other) for other in rooms):
                continue
            self._carve_room(grid, new_room)
            if rooms:
                prev_center = self._room_center(rooms[-1])
                new_center = self._room_center(new_room)
                self._carve_corridor(grid, prev_center, new_center)
            rooms.append(new_room)
        return grid, rooms
    def _carve_room(self, grid, room):
        x, y, w, h = room
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                grid[yy][xx] = config.TILE_FLOOR
    def _carve_corridor(self, grid, a, b):
        """L-shaped corridor between two points (horizontal then vertical)."""
        x1, y1 = a
        x2, y2 = b
        for xx in range(min(x1, x2), max(x1, x2) + 1):
            grid[y1][xx] = config.TILE_FLOOR
        for yy in range(min(y1, y2), max(y1, y2) + 1):
            grid[yy][x2] = config.TILE_FLOOR
    def _rooms_overlap(self, a, b):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return (ax - 1 < bx + bw + 1 and ax + aw + 1 > bx - 1 and
                ay - 1 < by + bh + 1 and ay + ah + 1 > by - 1)
    def _room_center(self, room):
        x, y, w, h = room
        return (x + w // 2, y + h // 2)
    def _farthest_room(self, grid, start, rooms):
        """Return the room whose center is farthest (BFS distance) from start."""
        best_room, best_dist = rooms[0], -1
        for room in rooms:
            center = self._room_center(room)
            dist = self._bfs_distance(grid, start, center)
            if dist is not None and dist > best_dist:
                best_dist = dist
                best_room = room
        return best_room
    def _pick_floor_in_room(self, grid, room):
        """Pick a random floor tile inside the room (prefers the center)."""
        x, y, w, h = room
        candidates = [(xx, yy)
                      for yy in range(y, y + h)
                      for xx in range(x, x + w)
                      if grid[yy][xx] == config.TILE_FLOOR]
        if not candidates:
            return None
        center = self._room_center(room)
        if center in candidates:
            return center
        return self.rng.choice(candidates)
    # ------------------------------------------------------------------ #
    # Pathfinding (guarantees start -> door connectivity)
    # ------------------------------------------------------------------ #
    def _has_path(self, grid, start, goal):
        seen, q = {start}, deque([start])
        while q:
            x, y = q.popleft()
            if (x, y) == goal:
                return True
            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                nx, ny = x + dx, y + dy
                if (0 <= nx < config.GRID_SIZE and 0 <= ny < config.GRID_SIZE
                        and grid[ny][nx] == config.TILE_FLOOR
                        and (nx, ny) not in seen):
                    seen.add((nx, ny))
                    q.append((nx, ny))
        return False
    def _bfs_distance(self, grid, start, goal):
        """Shortest path length start->goal over floor tiles, or None."""
        if start == goal:
            return 0
        dist = {start: 0}
        q = deque([start])
        while q:
            x, y = q.popleft()
            d = dist[(x, y)]
            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                nx, ny = x + dx, y + dy
                if (0 <= nx < config.GRID_SIZE and 0 <= ny < config.GRID_SIZE
                        and grid[ny][nx] == config.TILE_FLOOR
                        and (nx, ny) not in dist):
                    if (nx, ny) == goal:
                        return d + 1
                    dist[(nx, ny)] = d + 1
                    q.append((nx, ny))
        return None
    # ------------------------------------------------------------------ #
    # Entity placement
    # ------------------------------------------------------------------ #
    def _free_floor_tiles(self, grid, blocked):
        tiles = []
        for yy in range(config.GRID_SIZE):
            for xx in range(config.GRID_SIZE):
                pos = (xx, yy)
                if grid[yy][xx] == config.TILE_FLOOR and pos not in blocked:
                    tiles.append(pos)
        return tiles
    def _place_monsters(self, grid, level, start, door_pos):
        count = config.monsters_for_level(level)
        available = [t for t in config.MONSTER_TYPES if t[3] <= level]
        blocked = {start, door_pos}
        # keep the start tile's immediate neighborhood clear
        sx, sy = start
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            blocked.add((sx + dx, sy + dy))
        free = self._free_floor_tiles(grid, blocked)
        self.rng.shuffle(free)
        monsters = []
        for pos in free[:count]:
            name, base_hp, color, _min_level = self.rng.choice(available)
            hp = max(1, round(base_hp * config.monster_hp_scale(level)))
            monsters.append(Monster(pos[0], pos[1], name, hp, color))
        return monsters
    def _place_chests(self, grid, start, door_pos, monsters):
        blocked = {start, door_pos} | {m.position for m in monsters}
        free = self._free_floor_tiles(grid, blocked)
        self.rng.shuffle(free)
        chests = []
        for pos in free[:config.CHESTS_PER_LEVEL]:
            heal = self.rng.randint(config.CHEST_HEAL_MIN, config.CHEST_HEAL_MAX)
            chests.append(TreasureChest(pos[0], pos[1], heal))
        return chests
    # ------------------------------------------------------------------ #
    # Fallback (trivially guarantees a valid path)
    # ------------------------------------------------------------------ #
    def _fallback_level(self, level):
        grid = [[config.TILE_WALL for _ in range(config.GRID_SIZE)]
                for _ in range(config.GRID_SIZE)]
        for yy in range(2, config.GRID_SIZE - 2):
            for xx in range(2, config.GRID_SIZE - 2):
                grid[yy][xx] = config.TILE_FLOOR
        start = (config.GRID_SIZE // 2, config.GRID_SIZE - 4)
        door_pos = (config.GRID_SIZE // 2, 3)
        monsters = self._place_monsters(grid, level, start, door_pos)
        chests = self._place_chests(grid, start, door_pos, monsters)
        return LevelData(grid, start, Door(*door_pos), monsters, chests)