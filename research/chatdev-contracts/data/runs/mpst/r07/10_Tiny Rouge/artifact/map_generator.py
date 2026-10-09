'''
map_generator.py
Builds the fixed 80x80 dungeon floor for a given level.
Strategy:
1. Fill everything with floor, add a solid border wall.
2. Sprinkle random wall blobs for the maze-like feel.
3. BFS-check that start -> door is walkable; if not, carve an
   L-shaped corridor (random elbow) which mathematically guarantees
   at least one valid path (customer requirement).
4. Return the grid, the guaranteed path tiles and start/door spots
   so game.py can keep monsters off the safe route.
'''
import random
from collections import deque
from config import (
    GRID_SIZE, TILE_FLOOR, TILE_WALL, TILE_DOOR,
    WALL_BLOB_COUNT, WALL_BLOB_SIZE_MIN, WALL_BLOB_SIZE_MAX,
)
def generate_level(level, rng=None):
    '''Build one dungeon floor. Returns (grid, start, door, safe_path).'''
    if rng is None:
        rng = random.Random()
    grid = _blank_grid()
    start, door = _pick_start_door(rng)
    # Make sure the two anchor tiles are walkable before scattering walls.
    grid[start[1]][start[0]] = TILE_FLOOR
    grid[door[1]][door[0]] = TILE_DOOR
    _scatter_walls(grid, rng)
    # Re-stamp anchors in case a wall blob covered them.
    grid[start[1]][start[0]] = TILE_FLOOR
    grid[door[1]][door[0]] = TILE_DOOR
    path = _bfs_path(grid, start, door)
    if path is None:
        # Carve an L-shaped corridor: guarantees a valid path.
        _carve_l_path(grid, start, door, rng)
        path = _bfs_path(grid, start, door)
        # _carve_l_path guarantees connectivity, so path cannot be None here.
    return grid, start, door, path
def _blank_grid():
    '''All floor with a solid border wall.'''
    grid = [[TILE_FLOOR for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for i in range(GRID_SIZE):
        grid[0][i] = TILE_WALL
        grid[GRID_SIZE - 1][i] = TILE_WALL
        grid[i][0] = TILE_WALL
        grid[i][GRID_SIZE - 1] = TILE_WALL
    return grid
def _scatter_walls(grid, rng):
    '''Drop random rectangular blobs of wall for a maze-like feel.'''
    for _ in range(WALL_BLOB_COUNT):
        w = rng.randint(WALL_BLOB_SIZE_MIN, WALL_BLOB_SIZE_MAX)
        h = rng.randint(WALL_BLOB_SIZE_MIN, WALL_BLOB_SIZE_MAX)
        x0 = rng.randint(1, GRID_SIZE - 2 - (w - 1))
        y0 = rng.randint(1, GRID_SIZE - 2 - (h - 1))
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                grid[y][x] = TILE_WALL
def _bfs_path(grid, start, goal):
    '''
    Breadth-first search for the shortest walkable path.
    Floor AND door tiles are walkable (the door is the goal, so it must
    be reachable — this fixes the door-tile reachability bug).
    Returns a list of (x, y) tiles from start to goal, or None.
    '''
    if grid[start[1]][start[0]] == TILE_WALL or grid[goal[1]][goal[0]] == TILE_WALL:
        # start/goal should be floor; carve them just in case
        grid[start[1]][start[0]] = TILE_FLOOR
        grid[goal[1]][goal[0]] = TILE_FLOOR
    queue = deque([start])
    came = {start: None}
    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            path = []
            node = (x, y)
            while node is not None:
                path.append(node)
                node = came[node]
            path.reverse()
            return path
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nx, ny = x + dx, y + dy
            if (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE
                    and (nx, ny) not in came
                    and grid[ny][nx] in (TILE_FLOOR, TILE_DOOR)):
                came[(nx, ny)] = (x, y)
                queue.append((nx, ny))
    return None
def _carve_l_path(grid, start, goal, rng):
    '''
    Carve an L-shaped corridor (random elbow) between start and goal.
    Turning every tile on the corridor into floor mathematically
    guarantees at least one valid path (customer requirement).
    '''
    sx, sy = start
    gx, gy = goal
    if rng.random() < 0.5:
        # horizontal first, then vertical
        for x in range(min(sx, gx), max(sx, gx) + 1):
            grid[sy][x] = TILE_FLOOR
        for y in range(min(sy, gy), max(sy, gy) + 1):
            grid[y][gx] = TILE_FLOOR
    else:
        # vertical first, then horizontal
        for y in range(min(sy, gy), max(sy, gy) + 1):
            grid[y][sx] = TILE_FLOOR
        for x in range(min(sx, gx), max(sx, gx) + 1):
            grid[gy][x] = TILE_FLOOR
    # The door tile itself stays a door tile (walkable for BFS/movement).
    grid[goal[1]][goal[0]] = TILE_DOOR