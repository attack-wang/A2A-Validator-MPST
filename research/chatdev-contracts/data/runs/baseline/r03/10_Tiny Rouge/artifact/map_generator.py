'''
map_generator.py
Procedural generation of the fixed 80x80 tower floor.
A perfect maze is carved with recursive backtracking (which guarantees that
every floor tile is connected), then extra passages and open rooms are added
to create loops. A BFS from the start position is used to (a) prove that a
valid path to the door always exists - the door is placed on the farthest
reachable tile - and (b) distribute monsters and chests on reachable tiles.
'''
import random
from collections import deque
import config
from monster import Monster
from treasurechest import TreasureChest
from door import Door
def _create_grid():
    '''Return a fresh 80x80 grid filled with wall tiles.'''
    return [[config.TILE_WALL for _ in range(config.GRID_WIDTH)]
            for _ in range(config.GRID_HEIGHT)]
def _in_bounds(x, y):
    return 0 <= x < config.GRID_WIDTH and 0 <= y < config.GRID_HEIGHT
def _carve_maze(grid):
    '''Recursive-backtracking maze carving. Guarantees full connectivity of
    all odd-coordinate cells.'''
    stack = [(1, 1)]
    grid[1][1] = config.TILE_FLOOR
    visited = {(1, 1)}
    while stack:
        cx, cy = stack[-1]
        neighbours = []
        for dx, dy in ((0, -2), (0, 2), (-2, 0), (2, 0)):
            nx, ny = cx + dx, cy + dy
            if 1 <= nx < config.GRID_WIDTH - 1 and 1 <= ny < config.GRID_HEIGHT - 1 \
                    and (nx, ny) not in visited:
                neighbours.append((nx, ny))
        if neighbours:
            nx, ny = random.choice(neighbours)
            grid[(cy + ny) // 2][(cx + nx) // 2] = config.TILE_FLOOR
            grid[ny][nx] = config.TILE_FLOOR
            visited.add((nx, ny))
            stack.append((nx, ny))
        else:
            stack.pop()
def _carve_rooms(grid):
    '''Carve random open rectangular rooms into the maze to create open areas.'''
    for _ in range(config.ROOMS_PER_LEVEL):
        w = random.randint(config.ROOM_MIN_SIZE, config.ROOM_MAX_SIZE)
        h = random.randint(config.ROOM_MIN_SIZE, config.ROOM_MAX_SIZE)
        x = random.randint(1, config.GRID_WIDTH - w - 2)
        y = random.randint(1, config.GRID_HEIGHT - h - 2)
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                grid[yy][xx] = config.TILE_FLOOR
def _add_extra_passages(grid):
    '''Randomly remove walls between two floor tiles to create loops.'''
    removed = 0
    attempts = 0
    while removed < config.EXTRA_PASSAGES and attempts < config.EXTRA_PASSAGES * 10:
        attempts += 1
        x = random.randint(1, config.GRID_WIDTH - 2)
        y = random.randint(1, config.GRID_HEIGHT - 2)
        if grid[y][x] != config.TILE_WALL:
            continue
        # Only remove walls that separate two floor tiles (horizontal or vertical)
        if ((grid[y][x - 1] == config.TILE_FLOOR and grid[y][x + 1] == config.TILE_FLOOR) or
                (grid[y - 1][x] == config.TILE_FLOOR and grid[y + 1][x] == config.TILE_FLOOR)):
            grid[y][x] = config.TILE_FLOOR
            removed += 1
def _bfs_distances(grid, start):
    '''Breadth-first search from start. Returns dict {(x, y): distance} for
    every reachable floor tile.'''
    distances = {start: 0}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        d = distances[(x, y)]
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nx, ny = x + dx, y + dy
            if _in_bounds(nx, ny) and grid[ny][nx] == config.TILE_FLOOR \
                    and (nx, ny) not in distances:
                distances[(nx, ny)] = d + 1
                queue.append((nx, ny))
    return distances
def generate_level(level):
    '''Generate a complete level. Returns a dict with the grid, start position,
    door, monsters and chests. The door is placed on the farthest tile reachable
    from the start, which guarantees at least one valid path from start to door.'''
    while True:
        grid = _create_grid()
        _carve_maze(grid)
        _carve_rooms(grid)
        _add_extra_passages(grid)
        start = (1, 1)
        grid[start[1]][start[0]] = config.TILE_FLOOR
        distances = _bfs_distances(grid, start)
        if len(distances) < 60:  # too small / degenerate maze, regenerate
            continue
        # Place the door on the farthest reachable tile -> guaranteed path.
        door_pos = max(distances, key=distances.get)
        if door_pos == start:
            continue
        door = Door(door_pos[0], door_pos[1])
        # Candidate tiles for monsters / chests: reachable, not start, not door.
        candidates = [pos for pos, dist in distances.items()
                      if pos != start and pos != door_pos]
        monsters = _place_entities(
            candidates, distances,
            config.MONSTERS_PER_LEVEL_BASE + (level - 1) * 2,
            config.MONSTER_MIN_SPAWN_DISTANCE, start, door_pos)
        monster_objs = [Monster(x, y, random.choice(config.MONSTER_TYPES), level)
                        for (x, y) in monsters]
        chests = _place_entities(
            candidates, distances,
            config.CHESTS_PER_LEVEL_BASE + (level - 1),
            config.CHEST_MIN_SPAWN_DISTANCE, start, door_pos)
        chest_objs = [TreasureChest(x, y) for (x, y) in chests]
        return {"grid": grid, "start": start, "door": door,
                "monsters": monster_objs, "chests": chest_objs}