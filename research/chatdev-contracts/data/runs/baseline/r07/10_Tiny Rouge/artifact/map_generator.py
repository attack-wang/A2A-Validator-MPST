'''
map_generator.py
Procedural generation of the fixed 80x80 dungeon floor.
Guarantees:
  * Every room is connected with corridors, so a valid path from the
    player's start to the door always exists (verified with BFS).
  * Monsters and chests are only placed on tiles reachable from start.
'''
import random
from collections import deque
import settings
from entities import Monster, Chest, Door
class GameMap:
    '''Holds the tile grid plus every entity standing on it.'''
    def __init__(self, grid, start, door, monsters, chests):
        self.grid = grid
        self.start = start
        self.door = door
        self.monsters = monsters
        self.chests = chests
    def is_wall(self, x, y):
        return self.grid[y][x] == settings.WALL
    def in_bounds(self, x, y):
        return 0 <= x < settings.GRID_WIDTH and 0 <= y < settings.GRID_HEIGHT
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
def _carve_room(grid, x, y, w, h):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            grid[yy][xx] = settings.FLOOR
def _carve_h_corridor(grid, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        grid[y][x] = settings.FLOOR
def _carve_v_corridor(grid, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        grid[y][x] = settings.FLOOR
def _connect_rooms(grid, a, b):
    '''L-shaped corridor between the centers of rooms a and b.'''
    ax, ay = a
    bx, by = b
    if random.random() < 0.5:
        _carve_h_corridor(grid, ax, bx, ay)
        _carve_v_corridor(grid, ay, by, bx)
    else:
        _carve_v_corridor(grid, ay, by, ax)
        _carve_h_corridor(grid, ax, bx, by)
def _rooms_overlap(new_room, rooms, margin=1):
    '''Check whether new_room overlaps any existing room (with margin).'''
    x, y, w, h = new_room
    for (ox, oy, ow, oh) in rooms:
        if x < ox + ow + margin and ox < x + w + margin and \
           y < oy + oh + margin and oy < y + h + margin:
            return True
    return False
def bfs_reachable(grid, start):
    '''Flood fill of all floor tiles reachable from start (4-directional).'''
    sx, sy = start
    seen = {start}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nx, ny = x + dx, y + dy
            if (0 <= nx < settings.GRID_WIDTH and 0 <= ny < settings.GRID_HEIGHT
                    and grid[ny][nx] == settings.FLOOR and (nx, ny) not in seen):
                seen.add((nx, ny))
                queue.append((nx, ny))
    return seen
def bfs_distances(grid, start):
    '''BFS distance map from start to every reachable floor tile.'''
    dist = {start: 0}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        d = dist[(x, y)]
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nx, ny = x + dx, y + dy
            if (0 <= nx < settings.GRID_WIDTH and 0 <= ny < settings.GRID_HEIGHT
                    and grid[ny][nx] == settings.FLOOR and (nx, ny) not in dist):
                dist[(nx, ny)] = d + 1
                queue.append((nx, ny))
    return dist
def _random_floor_in_room(room):
    x, y, w, h = room
    return (random.randint(x, x + w - 1), random.randint(y, y + h - 1))
def _pick_monster(level):
    '''Choose a monster tier appropriate for the current dungeon level.'''
    max_tier = min(len(settings.MONSTER_TIERS) - 1, level - 1 + 2)
    tier = settings.MONSTER_TIERS[random.randint(0, max_tier)]
    hp = tier["base_hp"] + settings.MONSTER_HP_PER_LEVEL * (level - 1)
    return tier["name"], hp, tier["color"]
def generate_map(level):
    '''Generate one dungeon floor. Returns a GameMap instance.'''
    while True:  # regenerate in the (practically impossible) case validation fails
        grid = [[settings.WALL] * settings.GRID_WIDTH
                for _ in range(settings.GRID_HEIGHT)]
        # --- rooms -----------------------------------------------------
        room_count = random.randint(settings.ROOMS_PER_LEVEL_MIN,
                                    settings.ROOMS_PER_LEVEL_MAX)
        rooms = []
        attempts = 0
        while len(rooms) < room_count and attempts < 400:
            attempts += 1
            w = random.randint(settings.ROOM_MIN_SIZE, settings.ROOM_MAX_SIZE)
            h = random.randint(settings.ROOM_MIN_SIZE, settings.ROOM_MAX_SIZE)
            x = random.randint(1, settings.GRID_WIDTH - w - 2)
            y = random.randint(1, settings.GRID_HEIGHT - h - 2)
            new_room = (x, y, w, h)
            if _rooms_overlap(new_room, rooms):
                continue
            rooms.append(new_room)
            _carve_room(grid, x, y, w, h)
        if not rooms:  # degenerate placement, try a fresh layout
            continue
        centers = [(rx + rw // 2, ry + rh // 2) for (rx, ry, rw, rh) in rooms]
        # --- corridors: chain rooms + a few extra loops -----------------
        for i in range(1, len(centers)):
            _connect_rooms(grid, centers[i - 1], centers[i])
        for _ in range(settings.CORRIDOR_EXTRA_LINKS):
            if len(centers) >= 2:
                _connect_rooms(grid, random.choice(centers),
                               random.choice(centers))
        # --- start & door ----------------------------------------------
        start = centers[0]
        reachable = bfs_reachable(grid, start)
        dist = bfs_distances(grid, start)
        # door goes in the reachable room center farthest from the start
        door_candidates = [c for c in centers if c in dist and c != start]
        if not door_candidates:
            continue  # degenerate map, regenerate
        door_pos = max(door_candidates, key=lambda c: dist[c])
        # --- validation: path from start to door must exist -------------
        if door_pos not in dist:
            continue
        # --- monsters ---------------------------------------------------
        monster_count = settings.MONSTERS_BASE + settings.MONSTERS_PER_LEVEL * (level - 1)
        occupied = {start, door_pos}
        candidates = [tile for tile in reachable
                      if tile not in occupied and dist[tile] >= 2]
        random.shuffle(candidates)
        monsters = []
        for tile in candidates[:monster_count]:
            name, hp, color = _pick_monster(level)
            monsters.append(Monster(tile[0], tile[1], name, hp, color))
            occupied.add(tile)
        # --- chests -----------------------------------------------------
        chest_count = settings.CHESTS_BASE + (level - 1) // 2 * settings.CHESTS_PER_LEVEL
        chest_candidates = [tile for tile in candidates[len(monsters):]
                            if tile not in occupied and dist[tile] >= 2]
        random.shuffle(chest_candidates)
        chests = []
        for tile in chest_candidates[:chest_count]:
            chests.append(Chest(tile[0], tile[1]))
            occupied.add(tile)
        # --- final safety check -----------------------------------------
        reachable_final = bfs_reachable(grid, start)
        if door_pos not in reachable_final:
            continue  # practically impossible; regenerate to be safe
        door = Door(door_pos[0], door_pos[1])
        return GameMap(grid, start, door, monsters, chests)