'''Procedural generation of the fixed 80x80 tower floors.
The generator always guarantees at least one walkable route from the start
to the door, and additionally guarantees that the door can be reached
without being forced to fight any monster (monsters never fully block the
only corridor).
'''
import random
import settings
from pathfinding import bfs_path, reachable_cells, carve_path
from entities import Monster, TreasureChest
def _in_bounds(x, y):
    return 0 <= x < settings.GRID_SIZE and 0 <= y < settings.GRID_SIZE
def _random_floor_near(grid, tx, ty, radius=6):
    '''Find a walkable cell close to (tx, ty), searching outward in rings.'''
    for r in range(0, radius + 1):
        candidates = []
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                x, y = tx + dx, ty + dy
                if _in_bounds(x, y) and grid[y][x] == settings.FLOOR:
                    candidates.append((x, y))
        if candidates:
            return random.choice(candidates)
    return None
def _scatter_walls(grid):
    '''Randomly place small wall blocks/segments to create a maze-like layout.
    The outer border is left untouched (it is already solid wall).'''
    blocks = int(settings.GRID_SIZE * settings.GRID_SIZE * 0.05)
    for _ in range(blocks):
        x = random.randint(1, settings.GRID_SIZE - 2)
        y = random.randint(1, settings.GRID_SIZE - 2)
        length = random.randint(2, 6)
        horizontal = random.random() < 0.5
        for i in range(length):
            cx = x + (i if horizontal else 0)
            cy = y + (0 if horizontal else i)
            if _in_bounds(cx, cy):
                grid[cy][cx] = settings.WALL
def _generate_walls():
    '''Create a fresh 80x80 grid: solid border walls plus scattered obstacles.'''
    grid = [[settings.FLOOR] * settings.GRID_SIZE for _ in range(settings.GRID_SIZE)]
    for i in range(settings.GRID_SIZE):
        grid[0][i] = settings.WALL
        grid[settings.GRID_SIZE - 1][i] = settings.WALL
        grid[i][0] = settings.WALL
        grid[i][settings.GRID_SIZE - 1] = settings.WALL
    _scatter_walls(grid)
    return grid
def generate_level(level):
    '''Generate one tower floor. Returns (grid, start, door, monsters, chests).'''
    grid = _generate_walls()
    start = _random_floor_near(grid, 1, 1) or (1, 1)
    door = (_random_floor_near(grid, settings.GRID_SIZE - 2, settings.GRID_SIZE - 2)
            or (settings.GRID_SIZE - 2, settings.GRID_SIZE - 2))
    # The fallback start may sit on a wall - force it walkable.
    if grid[start[1]][start[0]] == settings.WALL:
        grid[start[1]][start[0]] = settings.FLOOR
    # Guarantee a walkable route between start and door.
    if bfs_path(grid, start, door) is None:
        carve_path(grid, start, door)
    grid[door[1]][door[0]] = settings.DOOR
    # All floor cells the player could possibly walk on.
    reachable = reachable_cells(grid, start)
    reachable.discard(start)
    reachable.discard(door)
    candidates = [
        (x, y) for (x, y) in reachable
        if abs(x - start[0]) + abs(y - start[1]) > 2   # nothing right on the spawn
    ]
    random.shuffle(candidates)
    monsters = {}
    chests = {}
    def path_still_open():
        return bfs_path(grid, start, door, blocked=set(monsters.keys())) is not None
    # Optional boss guarding the final floor (still must not seal the route).
    if level >= settings.MAX_LEVELS:
        for (x, y) in candidates:
            if abs(x - door[0]) + abs(y - door[1]) <= 6:
                base = settings.MONSTER_TYPES[-1]
                monsters[(x, y)] = Monster(base["name"], base["hp"],
                                           base["atk"], base["color"])
                if path_still_open():
                    candidates.remove((x, y))
                else:
                    del monsters[(x, y)]
                break
    desired_monsters = settings.BASE_MONSTERS_PER_LEVEL + level
    placed = 0
    for cell in candidates:
        if placed >= desired_monsters:
            break
        monsters[cell] = Monster.spawn(level)
        if not path_still_open():
            del monsters[cell]      # this monster would seal the only route
            continue
        placed += 1
    # Chests go on any remaining free cell (they never block movement).
    free = [c for c in candidates if c not in monsters]
    for cell in random.sample(free, min(settings.BASE_CHESTS_PER_LEVEL, len(free))):
        chests[cell] = TreasureChest()
    return grid, start, door, monsters, chests