"""Procedural generation of the fixed 80x80 tower floors.
Each floor guarantees at least one valid path from the start position to
the door: a biased random walk carves the main corridor, extra rooms are
carved on top, and a BFS check verifies connectivity (regenerating the
floor if verification ever fails).
"""
import random
from collections import deque
import settings
from entities import Monster
class Level:
    """One floor of the tower: grid, monsters, chests, start and door."""
    def __init__(self, number, rng=None):
        self.number = number
        self.rng = rng if rng is not None else random
        self.size = settings.MAP_SIZE
        self.start = (2, 2)                    # (row, col) top-left area
        self.door = (self.size - 3, self.size - 3)  # bottom-right area
        self.grid = []
        self.monsters = {}   # (row, col) -> Monster
        self.chests = set()  # {(row, col), ...}
        self.generate()
    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------
    def generate(self):
        """Build the floor; retry until BFS confirms start->door path."""
        for _ in range(settings.MAX_GEN_ATTEMPTS):
            grid = [[settings.TILE_WALL] * self.size for _ in range(self.size)]
            self._carve_corridor(grid)
            self._carve_rooms(grid)
            if self._path_exists(grid, self.start, self.door):
                self.grid = grid
                self._place_entities()
                return
        raise RuntimeError("Level generation failed after max attempts")
    def _carve_corridor(self, grid):
        """Biased random walk from start to door; guarantees connectivity."""
        r, c = self.start
        grid[r][c] = settings.TILE_FLOOR
        tr, tc = self.door
        grid[tr][tc] = settings.TILE_FLOOR
        while (r, c) != self.door:
            if self.rng.random() < 0.65:       # bias toward the door
                if abs(tr - r) >= abs(tc - c):
                    r += 1 if tr > r else -1
                else:
                    c += 1 if tc > c else -1
            else:                               # occasional random sidestep
                dr, dc = self.rng.choice(((-1, 0), (1, 0), (0, -1), (0, 1)))
                nr, nc = r + dr, c + dc
                if 1 <= nr < self.size - 1 and 1 <= nc < self.size - 1:
                    r, c = nr, nc
            grid[r][c] = settings.TILE_FLOOR
    def _carve_rooms(self, grid, count=None):
        """Carve small rectangular rooms to open up the floor."""
        if count is None:
            count = settings.ROOMS_PER_LEVEL
        rows, cols = len(grid), len(grid[0])
        for _ in range(count):
            h = self.rng.randint(4, 9)
            w = self.rng.randint(4, 9)
            r = self.rng.randint(1, rows - 1 - h)
            c = self.rng.randint(1, cols - 1 - w)
            for rr in range(r, r + h):
                for cc in range(c, c + w):
                    grid[rr][cc] = settings.TILE_FLOOR
    def _path_exists(self, grid, start, door):
        """BFS over non-wall tiles; True if door reachable from start."""
        rows, cols = len(grid), len(grid[0])
        visited = [[False] * cols for _ in range(rows)]
        queue = deque([start])
        visited[start[0]][start[1]] = True
        while queue:
            r, c = queue.popleft()
            if (r, c) == door:
                return True
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols \
                        and not visited[nr][nc] \
                        and grid[nr][nc] != settings.TILE_WALL:
                    visited[nr][nc] = True
                    queue.append((nr, nc))
        return False
    def _place_entities(self):
        """Scatter monsters and chests on free floor tiles."""
        free = [(r, c)
                for r in range(self.size) for c in range(self.size)
                if self.grid[r][c] == settings.TILE_FLOOR
                and (r, c) not in (self.start, self.door)]
        self.rng.shuffle(free)
        n_monsters = min(len(free), self.rng.randint(
            settings.MONSTERS_PER_LEVEL_BASE,
            settings.MONSTERS_PER_LEVEL_BASE + settings.MONSTERS_PER_LEVEL_SPREAD))
        for _ in range(n_monsters):
            pos = free.pop()
            self.monsters[pos] = self._make_monster()
        n_chests = min(len(free), self.rng.randint(
            settings.CHESTS_PER_LEVEL_BASE,
            settings.CHESTS_PER_LEVEL_BASE + settings.CHESTS_PER_LEVEL_SPREAD))
        for _ in range(n_chests):
            self.chests.add(free.pop())
    def _make_monster(self):
        """Pick a monster whose difficulty scales with the floor number."""
        max_index = min(len(settings.MONSTER_TYPES) - 1, self.number - 1)
        name, base_hp = self.rng.choice(settings.MONSTER_TYPES[:max_index + 1])
        hp = base_hp + self.rng.randint(0, 5) + (self.number - 1) * 5
        return Monster(name, hp)
    # ------------------------------------------------------------------
    # Queries / mutations used by the game loop
    # ------------------------------------------------------------------
    def is_wall(self, r, c):
        """True if (r, c) is outside the map or a wall tile."""
        if not (0 <= r < self.size and 0 <= c < self.size):
            return True
        return self.grid[r][c] == settings.TILE_WALL
    def monster_at(self, r, c):
        return self.monsters.get((r, c))
    def chest_at(self, r, c):
        return (r, c) in self.chests
    def remove_monster(self, r, c):
        self.monsters.pop((r, c), None)
    def remove_chest(self, r, c):
        self.chests.discard((r, c))
    def adjacent_monster(self, r, c):
        """First monster orthogonally adjacent to (r, c), for the UI."""
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            m = self.monster_at(r + dr, c + dc)
            if m:
                return m
        return None