"""Procedural generation of the fixed 80x80 tower floor.
Generation pipeline (connectivity-safe by construction):
1. Fill grid with walls.
2. Recursive-backtracking maze over odd coordinates -> every floor cell
   reachable (spanning tree).
3. Carve random rooms (only removes walls -> connectivity preserved).
4. Remove extra walls between floors to create loops (multiple routes).
5. BFS from the start; place the door on the farthest reachable floor tile
   (guarantees a valid start->door path).
6. Spawn monsters/chests on reachable floor tiles away from the start.
7. Verify with BFS that the door is reachable; regenerate otherwise
   (defensive; should never trigger).
"""
import random
from collections import deque
import config
from entities import Monster, TreasureChest
from gamemap import GameMap
def _carve_maze(grid, rng):
    """Step 2: recursive-backtracking maze on odd coordinates."""
    height = config.GRID_HEIGHT
    width = config.GRID_WIDTH
    start_x, start_y = 1, 1
    grid[start_y][start_x] = config.TILE_FLOOR
    stack = [(start_x, start_y)]
    visited = {(start_x, start_y)}
    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)):
            nx, ny = x + dx, y + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and (nx, ny) not in visited:
                neighbors.append((nx, ny))
        if not neighbors:
            stack.pop()
            continue
        nx, ny = rng.choice(neighbors)
        grid[y + (ny - y) // 2][x + (nx - x) // 2] = config.TILE_FLOOR
        grid[ny][nx] = config.TILE_FLOOR
        visited.add((nx, ny))
        stack.append((nx, ny))
def _carve_rooms(grid, rng):
    """Step 3: carve random rooms; removing walls never breaks connectivity."""
    for _ in range(config.MAZE_ROOMS):
        w = rng.randrange(config.ROOM_MIN_SIZE, config.ROOM_MAX_SIZE + 1)
        h = rng.randrange(config.ROOM_MIN_SIZE, config.ROOM_MAX_SIZE + 1)
        x = rng.randrange(1, config.GRID_WIDTH - w - 1)
        y = rng.randrange(1, config.GRID_HEIGHT - h - 1)
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                grid[yy][xx] = config.TILE_FLOOR
def _add_loops(grid, rng):
    """Step 4: remove walls separating two floors to create cycles (multiple routes)."""
    removed, tries = 0, 0
    while removed < config.EXTRA_LOOPS and tries < config.EXTRA_LOOPS * 20:
        tries += 1
        x = rng.randrange(1, config.GRID_WIDTH - 1)
        y = rng.randrange(1, config.GRID_HEIGHT - 1)
        if grid[y][x] != config.TILE_WALL:
            continue
        if grid[y][x - 1] != config.TILE_WALL and grid[y][x + 1] != config.TILE_WALL:
            grid[y][x] = config.TILE_FLOOR
            removed += 1
        elif grid[y - 1][x] != config.TILE_WALL and grid[y + 1][x] != config.TILE_WALL:
            grid[y][x] = config.TILE_FLOOR
            removed += 1
def _bfs_distances(grid, start):
    """BFS distance map from start over all non-wall tiles."""
    dist = {start: 0}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if (0 <= nx < config.GRID_WIDTH and 0 <= ny < config.GRID_HEIGHT
                    and grid[ny][nx] != config.TILE_WALL and (nx, ny) not in dist):
                dist[(nx, ny)] = dist[(x, y)] + 1
                q.append((nx, ny))
    return dist
def generate_level(level, rng=None):
    """Generate one floor; door on the farthest BFS tile guarantees a start->door path."""
    rng = rng if rng is not None else random.Random()
    while True:  # defensive regeneration
        grid = [[config.TILE_WALL] * config.GRID_WIDTH
                for _ in range(config.GRID_HEIGHT)]
        start = (1, 1)
        _carve_maze(grid, rng)
        _carve_rooms(grid, rng)
        _add_loops(grid, rng)
        dist = _bfs_distances(grid, start)
        if len(dist) < 50:  # degenerate map -> retry
            continue
        door = max(dist, key=dist.get)  # Step 5: farthest reachable tile
        grid[door[1]][door[0]] = config.TILE_DOOR
        # Step 6: spawn on reachable tiles away from start, never on the door
        candidates = [p for p, d in dist.items()
                      if d >= config.MONSTER_MIN_DIST_FROM_START and p != door]
        rng.shuffle(candidates)
        monsters, chests = [], []
        n_m = config.MONSTERS_PER_LEVEL_BASE + level
        n_c = config.CHESTS_PER_LEVEL_BASE + level // 2
        for (x, y) in candidates:
            if len(monsters) < n_m:
                hp = rng.randint(config.MONSTER_HP_BASE_MIN + level * config.MONSTER_HP_LEVEL_SCALE,
                                 config.MONSTER_HP_BASE_MAX + level * config.MONSTER_HP_LEVEL_SCALE)
                monsters.append(Monster(x, y, hp))
            elif len(chests) < n_c:
                chests.append(TreasureChest(x, y))
            else:
                break
        if door in _bfs_distances(grid, start):  # Step 7: verify (defensive)
            return GameMap(grid, start, door, monsters, chests)