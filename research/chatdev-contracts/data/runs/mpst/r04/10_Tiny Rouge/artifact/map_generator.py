'''
map_generator.py
Procedural generation of the fixed 80x80 grid map with a guaranteed
start->door path. Rooms are carved randomly and chained together with
L-shaped corridors, so connectivity is ensured by construction; a BFS
check (`GameMap.path_exists`) verifies it anyway, and a straight
corridor fallback covers the (practically impossible) failure case.
'''
import random
from collections import deque
import config
from entities import Monster, TreasureChest
class GameMap:
    """Container for one dungeon level: grid + entities + BFS utilities."""
    def __init__(self, level, grid, start, door, monsters, chests):
        self.level = level
        self.grid = grid                      # grid[y][x] -> WALL / FLOOR
        self.start = start                    # (x, y)
        self.door = door                      # (x, y)
        self.monsters = {m.position: m for m in monsters}   # (x,y) -> Monster
        self.chests = {c.position: c for c in chests}       # (x,y) -> TreasureChest
    # -- tile helpers -------------------------------------------------------
    def in_bounds(self, x, y):
        return 0 <= x < config.MAP_WIDTH and 0 <= y < config.MAP_HEIGHT
    def is_floor(self, x, y):
        return self.in_bounds(x, y) and self.grid[y][x] == config.FLOOR
    # -- entity lookups -----------------------------------------------------
    def monster_at(self, x, y):
        """Return the Monster at (x, y) or None."""
        return self.monsters.get((x, y))
    def chest_at(self, x, y):
        """Return the TreasureChest at (x, y) or None."""
        return self.chests.get((x, y))
    def remove_monster(self, monster):
        self.monsters.pop(monster.position, None)
    def remove_chest(self, chest):
        self.chests.pop(chest.position, None)
    # -- pathfinding --------------------------------------------------------
    def reachable_from(self, start):
        """Set of floor tiles reachable from `start` via 4-directional moves."""
        seen = {start}
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            for dx, dy in ((0, -1), (-1, 0), (0, 1), (1, 0)):
                nx, ny = x + dx, y + dy
                if self.is_floor(nx, ny) and (nx, ny) not in seen:
                    seen.add((nx, ny))
                    queue.append((nx, ny))
        return seen
    def path_exists(self):
        """True when the door is reachable from the start (BFS over floors)."""
        return self.door in self.reachable_from(self.start)
class MapGenerator:
    """Builds GameMap instances for a given tower level."""
    MAX_GENERATION_ATTEMPTS = config.MAX_GENERATION_ATTEMPTS
    # Monster names ordered by toughness; index picked from monster HP.
    MONSTER_NAMES = (
        "Slime", "Bat", "Skeleton", "Zombie", "Ghost",
        "Demon", "Golem", "Wizard", "Basilisk", "Dragon Lord",
    )
    def generate(self, level):
        """Generate a fully populated level. Never returns an unconnected map."""
        for _ in range(self.MAX_GENERATION_ATTEMPTS):
            grid, start, door = self._carve()
            game_map = GameMap(level, grid, start, door, [], [])
            reachable = game_map.reachable_from(start)
            if door not in reachable:
                continue  # safety net; corridors should make this impossible
            monsters, chests = self._place_entities(game_map, reachable, level)
            game_map.monsters = {m.position: m for m in monsters}
            game_map.chests = {c.position: c for c in chests}
            return game_map
        # Fallback (practically unreachable): a straight guaranteed corridor.
        return self._fallback_map(level)
    # -- carving ------------------------------------------------------------
    def _carve(self):
        """Random rooms + L-corridors between consecutive room centers."""
        grid = [[config.WALL] * config.MAP_WIDTH for _ in range(config.MAP_HEIGHT)]
        rooms = []
        attempts = 0
        target_rooms = random.randint(config.ROOMS_MIN, config.ROOMS_MAX)
        while len(rooms) < target_rooms and attempts < 300:
            attempts += 1
            rw = random.randint(config.ROOM_SIZE_MIN, config.ROOM_SIZE_MAX)
            rh = random.randint(config.ROOM_SIZE_MIN, config.ROOM_SIZE_MAX)
            x0 = random.randint(1, config.MAP_WIDTH - rw - 1)
            y0 = random.randint(1, config.MAP_HEIGHT - rh - 1)
            rect = (x0, y0, rw, rh)
            if any(self._rooms_overlap(rect, other, margin=1) for other in rooms):
                continue
            rooms.append(rect)
            self._carve_room(grid, x0, y0, rw, rh)
        # Chain every room to the previous one -> whole map is connected.
        for i in range(1, len(rooms)):
            cx1, cy1 = self._room_center(rooms[i - 1])
            cx2, cy2 = self._room_center(rooms[i])
            self._carve_corridor(grid, cx1, cy1, cx2, cy2)
        start = self._room_center(rooms[0])
        door = self._room_center(rooms[-1])
        return grid, start, door
    @staticmethod
    def _room_center(room):
        x0, y0, rw, rh = room
        return (x0 + rw // 2, y0 + rh // 2)
    @staticmethod
    def _rooms_overlap(a, b, margin=0):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return (ax - margin < bx + bw and bx - margin < ax + aw and
                ay - margin < by + bh and by - margin < ay + ah)
    @staticmethod
    def _carve_room(grid, x0, y0, rw, rh):
        for y in range(y0, y0 + rh):
            for x in range(x0, x0 + rw):
                grid[y][x] = config.FLOOR
    def _carve_corridor(self, grid, x1, y1, x2, y2):
        """L-shaped corridor; randomize horizontal/vertical order for variety."""
        if random.random() < 0.5:
            self._carve_h(grid, x1, x2, y1)
            self._carve_v(grid, y1, y2, x2)
        else:
            self._carve_v(grid, y1, y2, x1)
            self._carve_h(grid, x1, x2, y2)
    @staticmethod
    def _carve_h(grid, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            if 0 < x < config.MAP_WIDTH - 1 and 0 < y < config.MAP_HEIGHT - 1:
                grid[y][x] = config.FLOOR
    @staticmethod
    def _carve_v(grid, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if 0 < x < config.MAP_WIDTH - 1 and 0 < y < config.MAP_HEIGHT - 1:
                grid[y][x] = config.FLOOR
    # -- entities -----------------------------------------------------------
    def _place_entities(self, game_map, reachable, level):
        """Scatter monsters and chests on reachable floor tiles.
        Tiles within Chebyshev distance 2 of the start and the door tile
        itself are kept clear so the player never spawns in danger and the
        exit is never blocked by a mandatory fight.
        """
        start = game_map.start
        door = game_map.door
        excluded = set()
        sx, sy = start
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                excluded.add((sx + dx, sy + dy))
        excluded.add(door)
        candidates = [pos for pos in reachable if pos not in excluded]
        random.shuffle(candidates)
        monster_count = min(
            config.MONSTERS_PER_LEVEL_BASE + (level - 1) * config.MONSTERS_PER_LEVEL_INCREMENT,
            config.MONSTERS_MAX,
        )
        chest_count = min(
            config.CHESTS_PER_LEVEL_BASE + (level - 1) * config.CHESTS_PER_LEVEL_INCREMENT,
            config.CHESTS_MAX,
        )
        monster_count = min(monster_count, len(candidates))
        chest_count = min(chest_count, max(0, len(candidates) - monster_count))
        monsters = []
        for _ in range(monster_count):
            pos = candidates.pop()
            hp = self._monster_hp(level)
            monsters.append(Monster(pos[0], pos[1], hp, self._monster_name(hp)))
        chests = []
        for _ in range(chest_count):
            pos = candidates.pop()
            heal = random.randint(config.CHEST_HEAL_MIN, config.CHEST_HEAL_MAX)
            chests.append(TreasureChest(pos[0], pos[1], heal))
        return monsters, chests
    def _monster_hp(self, level):
        return (random.randint(config.MONSTER_HP_BASE_MIN, config.MONSTER_HP_BASE_MAX) +
                (level - 1) * config.MONSTER_HP_LEVEL_SCALE)
    def _monster_name(self, hp):
        index = min(hp // 10, len(self.MONSTER_NAMES) - 1)
        return self.MONSTER_NAMES[index]
    # -- fallback -----------------------------------------------------------
    def _fallback_map(self, level):
        """Straight corridor across the middle: trivially connected."""
        grid = [[config.WALL] * config.MAP_WIDTH for _ in range(config.MAP_HEIGHT)]
        y = config.MAP_HEIGHT // 2
        for x in range(1, config.MAP_WIDTH - 1):
            grid[y][x] = config.FLOOR
        start = (1, y)
        door = (config.MAP_WIDTH - 2, y)
        game_map = GameMap(level, grid, start, door, [], [])
        monsters, chests = self._place_entities(game_map, game_map.reachable_from(start), level)
        game_map.monsters = {m.position: m for m in monsters}
        game_map.chests = {c.position: c for c in chests}
        return game_map