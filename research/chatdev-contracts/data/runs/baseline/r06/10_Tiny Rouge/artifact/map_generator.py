'''
map_generator.py
Procedural generation of the fixed 80x80 grid map with guaranteed start-to-door path.
'''
import random
from collections import deque
import config
from entities import Monster
from chest import Chest
class MapData:
    """Container for a generated level: grid, spawn, door, monsters, chests."""
    def __init__(self, grid, start, door, monsters, chests):
        self.grid = grid
        self.start = start
        self.door = door
        self.monsters = monsters   # dict[(x, y)] -> Monster
        self.chests = chests       # dict[(x, y)] -> Chest
class MapGenerator:
    """Generates room-and-corridor maps on a fixed GRID_SIZE x GRID_SIZE grid.
    The map is built from an 8x8 lattice of cells; each cell contains a room,
    and cells are connected by carved corridors following a random spanning
    tree (plus extra loops). Because every room is connected, a path from the
    start to the door always exists; BFS is used to verify the path and to
    place the door far from the start.
    """
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
    # --- public API ---------------------------------------------------
    def generate(self, level):
        """Generate a MapData for the given level number."""
        while True:
            grid, room_centers = self._carve_rooms_and_corridors()
            start = self.rng.choice(room_centers)
            dist = self._bfs_distances(grid, start)
            reachable = [pos for pos, d in dist.items() if d is not None]
            # door: farthest reachable floor tile from the start
            door = max(reachable, key=lambda p: dist[p])
            # verify path (defensive; guaranteed by construction)
            if self._path_exists(grid, start, door):
                break
        monsters = self._place_monsters(grid, level, start, door, dist)
        chests = self._place_chests(grid, start, door, set(monsters.keys()))
        return MapData(grid, start, door, monsters, chests)
    # --- map carving ----------------------------------------------------
    def _carve_rooms_and_corridors(self):
        """Carve one random room per lattice cell and connect all cells with
        corridors following a random spanning tree (plus extra loops).
        Returns (grid, list_of_room_centers).
        """
        cells = config.GRID_SIZE // config.CELL_SIZE  # 8x8 generation cells
        grid = [[config.WALL] * config.GRID_SIZE for _ in range(config.GRID_SIZE)]
        centers = [[None] * cells for _ in range(cells)]
        # 1) one random room inside each cell (1+ wall tiles remain between cells)
        for cy in range(cells):
            for cx in range(cells):
                w = self.rng.randint(3, config.CELL_SIZE - 2)
                h = self.rng.randint(3, config.CELL_SIZE - 2)
                x0 = cx * config.CELL_SIZE + self.rng.randint(0, config.CELL_SIZE - w - 1)
                y0 = cy * config.CELL_SIZE + self.rng.randint(0, config.CELL_SIZE - h - 1)
                for y in range(y0, y0 + h):
                    for x in range(x0, x0 + w):
                        grid[y][x] = config.FLOOR
                centers[cy][cx] = (x0 + w // 2, y0 + h // 2)
        # 2) random spanning tree (iterative DFS) -> every room is connected
        first = (self.rng.randrange(cells), self.rng.randrange(cells))
        visited = {first}
        stack = [first]
        tree_edges = []
        while stack:
            cx, cy = stack[-1]
            neighbours = [(cx + dx, cy + dy) for dx, dy in
                          ((1, 0), (-1, 0), (0, 1), (0, -1))
                          if 0 <= cx + dx < cells and 0 <= cy + dy < cells
                          and (cx + dx, cy + dy) not in visited]
            if neighbours:
                nxt = self.rng.choice(neighbours)
                visited.add(nxt)
                tree_edges.append(((cx, cy), nxt))
                stack.append(nxt)
            else:
                stack.pop()
        # 3) a few extra edges for loops (more interesting routes)
        all_edges = set()
        for cy in range(cells):
            for cx in range(cells):
                for dx, dy in ((1, 0), (0, 1)):
                    nx, ny = cx + dx, cy + dy
                    if nx < cells and ny < cells:
                        all_edges.add(((cx, cy), (nx, ny)))
        extra = [e for e in all_edges if e not in tree_edges and (e[1], e[0]) not in tree_edges]
        self.rng.shuffle(extra)
        for e in extra[: self.rng.randint(3, 6)]:
            tree_edges.append(e)
        # 4) carve L-shaped corridors between connected room centers
        for (a, b) in tree_edges:
            self._carve_corridor(grid, centers[a[1]][a[0]], centers[b[1]][b[0]])
        return grid, [centers[cy][cx] for cy in range(cells) for cx in range(cells)]
    def _carve_corridor(self, grid, a, b):
        """Carve an L-shaped corridor between two points (random elbow order)."""
        ax, ay = a
        bx, by = b
        if self.rng.random() < 0.5:
            self._carve_line(grid, ax, ay, bx, ay)
            self._carve_line(grid, bx, ay, bx, by)
        else:
            self._carve_line(grid, ax, ay, ax, by)
            self._carve_line(grid, ax, by, bx, by)
    def _carve_line(self, grid, x0, y0, x1, y1):
        """Set FLOOR along a straight horizontal or vertical segment."""
        x0, x1 = min(x0, x1), max(x0, x1)
        y0, y1 = min(y0, y1), max(y0, y1)
        for x in range(x0, x1 + 1):
            grid[y0][x] = config.FLOOR
        for y in range(y0, y1 + 1):
            grid[y][x1] = config.FLOOR
    # --- BFS helpers ------------------------------------------------------
    def _bfs_distances(self, grid, start):
        """BFS over floor tiles; returns dict[(x, y)] -> distance or None."""
        dist = {(start[0], start[1]): 0}
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < config.GRID_SIZE and 0 <= ny < config.GRID_SIZE \
                        and grid[ny][nx] != config.WALL and (nx, ny) not in dist:
                    dist[(nx, ny)] = dist[(x, y)] + 1
                    queue.append((nx, ny))
        # mark all floor tiles as reachable/unreachable
        for y in range(config.GRID_SIZE):
            for x in range(config.GRID_SIZE):
                if grid[y][x] != config.WALL and (x, y) not in dist:
                    dist[(x, y)] = None
        return dist
    def _path_exists(self, grid, start, goal):
        """Defensive BFS check that a wall-free path exists from start to goal."""
        if grid[goal[1]][goal[0]] == config.WALL:
            return False
        seen = {start}
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                return True
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < config.GRID_SIZE and 0 <= ny < config.GRID_SIZE \
                        and grid[ny][nx] != config.WALL and (nx, ny) not in seen:
                    seen.add((nx, ny))
                    queue.append((nx, ny))
        return False
    # --- entity placement ---------------------------------------------------
    def _floor_candidates(self, grid, dist, exclude):
        """All reachable floor tiles except the excluded positions."""
        candidates = []
        for (x, y), d in dist.items():
            if d is not None and grid[y][x] == config.FLOOR and (x, y) not in exclude:
                candidates.append((x, y))
        return candidates
    def _place_monsters(self, grid, level, start, door, dist):
        """Scatter monsters on reachable floor tiles away from start/door."""
        exclude = {start, door}
        # keep a safe radius around the spawn
        for y in range(config.GRID_SIZE):
            for x in range(config.GRID_SIZE):
                if dist.get((x, y)) is not None and dist[(x, y)] <= config.SAFE_RADIUS:
                    exclude.add((x, y))
        candidates = self._floor_candidates(grid, dist, exclude)
        self.rng.shuffle(candidates)
        monsters = {}
        scale = 1.0 + (level - 1) * config.MONSTER_HP_SCALE_PER_LEVEL
        for pos in candidates[: config.MONSTERS_PER_LEVEL]:
            name, base_hp, color = self.rng.choice(config.MONSTER_TYPES)
            hp = max(1, int(round(base_hp * scale)))
            monsters[pos] = Monster(name, hp, color, pos[0], pos[1])
        return monsters
    def _place_chests(self, grid, start, door, monster_positions):
        """Place chests on free reachable floor tiles (not start/door/monster)."""
        dist = self._bfs_distances(grid, start)
        exclude = {start, door} | monster_positions
        candidates = self._floor_candidates(grid, dist, exclude)
        self.rng.shuffle(candidates)
        chests = {}
        for pos in candidates[: config.CHESTS_PER_LEVEL]:
            heal = self.rng.randint(config.CHEST_HEAL_MIN, config.CHEST_HEAL_MAX)
            chests[pos] = Chest(pos[0], pos[1], heal)
        return chests