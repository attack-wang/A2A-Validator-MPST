'''
map_generator.py
Procedural generation of the 80x80 tower floor.
Generation pipeline (connectivity is guaranteed by construction):
1. Fill the grid with walls.
2. Carve a perfect maze with the recursive-backtracker algorithm
   (every floor cell becomes reachable).
3. "Braid" the maze by randomly opening some walls so the floor feels
   more like an open tower floor instead of a strict labyrinth.
4. Carve a few open rooms.
5. Run a BFS from the start to obtain every reachable tile and its
   distance; the door is placed on the farthest reachable tile, which
   guarantees at least one valid path from start to door.
6. Monsters and treasures are dropped on random reachable floor tiles.
'''
import random
from collections import deque
import settings
from entities import Monster, Treasure
class MapGenerator:
    def __init__(self, level=1, rng=None):
        """Store the current level and the random source used for generation."""
        self.level = level
        self.rng = rng or random.Random()
    def generate(self):
        """Run the full pipeline and return grid, start, door, monsters and treasures."""
        grid = self._carve_maze()
        self._braid(grid)
        self._carve_rooms(grid)
        start = (1, 1)
        distances = self._bfs_distances(grid, start)
        door = self._place_door(grid, distances)
        monsters = self._place_monsters(grid, distances, door, start)
        treasures = self._place_treasures(grid, distances, door, start, monsters)
        return {
            "grid": grid,
            "start": start,
            "door": door,
            "monsters": monsters,
            "treasures": treasures,
        }
    def _carve_maze(self):
        """Recursive-backtracker maze on odd coordinates; every floor cell reachable."""
        grid = [[settings.WALL for _ in range(settings.GRID_WIDTH)]
                for _ in range(settings.GRID_HEIGHT)]
        grid[1][1] = settings.FLOOR
        stack = [(1, 1)]
        while stack:
            x, y = stack[-1]
            neighbors = []
            for dx, dy in ((0, -2), (0, 2), (-2, 0), (2, 0)):
                nx, ny = x + dx, y + dy
                if (1 <= nx < settings.GRID_WIDTH - 1 and
                        1 <= ny < settings.GRID_HEIGHT - 1 and
                        grid[ny][nx] == settings.WALL):
                    neighbors.append((nx, ny))
            if neighbors:
                nx, ny = self.rng.choice(neighbors)
                grid[y + (ny - y) // 2][x + (nx - x) // 2] = settings.FLOOR
                grid[ny][nx] = settings.FLOOR
                stack.append((nx, ny))
            else:
                stack.pop()
        return grid
    def _braid(self, grid):
        """Randomly open dead-end walls so the floor is less corridor-like."""
        for y in range(1, settings.GRID_HEIGHT - 1):
            for x in range(1, settings.GRID_WIDTH - 1):
                if grid[y][x] != settings.FLOOR:
                    continue
                wall_dirs = [(dx, dy) for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0))
                             if grid[y + dy][x + dx] == settings.WALL]
                if len(wall_dirs) >= 3 and self.rng.random() < settings.MAZE_BRAID_CHANCE:
                    openable = [(x + dx, y + dy) for dx, dy in wall_dirs
                                if 0 < x + 2 * dx < settings.GRID_WIDTH - 1 and
                                0 < y + 2 * dy < settings.GRID_HEIGHT - 1 and
                                grid[y + 2 * dy][x + 2 * dx] == settings.FLOOR]
                    if openable:
                        wx, wy = self.rng.choice(openable)
                        grid[wy][wx] = settings.FLOOR
    def _carve_rooms(self, grid):
        """Carve a few odd-aligned rectangular rooms onto the maze."""
        for _ in range(settings.ROOMS_PER_LEVEL):
            w = self.rng.randint(3, 9) | 1   # odd width
            h = self.rng.randint(3, 9) | 1   # odd height
            x = self.rng.randrange(1, settings.GRID_WIDTH - w, 2)
            y = self.rng.randrange(1, settings.GRID_HEIGHT - h, 2)
            for yy in range(y, y + h):
                for xx in range(x, x + w):
                    grid[yy][xx] = settings.FLOOR
    def _bfs_distances(self, grid, start):
        """BFS from start; returns {position: distance} for every reachable floor tile."""
        dist = {start: 0}
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            d = dist[(x, y)]
            for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                nx, ny = x + dx, y + dy
                if (0 <= nx < settings.GRID_WIDTH and
                        0 <= ny < settings.GRID_HEIGHT and
                        grid[ny][nx] == settings.FLOOR and
                        (nx, ny) not in dist):
                    dist[(nx, ny)] = d + 1
                    queue.append((nx, ny))
        return dist
    def _place_door(self, grid, distances):
        """Put the door on the farthest reachable tile -> a path from start always exists."""
        door = max(distances, key=distances.get)
        grid[door[1]][door[0]] = settings.DOOR
        return door
    def _place_monsters(self, grid, distances, door, start):
        """Drop monsters on random reachable floor tiles away from the start."""
        count = settings.MONSTERS_BASE + settings.MONSTERS_PER_LEVEL * (self.level - 1)
        candidates = [pos for pos, d in distances.items() if d >= 4 and pos != door]
        self.rng.shuffle(candidates)
        monsters = []
        for pos in candidates[:count]:
            template = self.rng.choice(settings.MONSTER_TYPES)
            hp = template["hp"] + settings.MONSTER_HP_SCALING * (self.level - 1)
            monsters.append(Monster(pos[0], pos[1], template["name"], hp, template["color"]))
        return monsters
    def _place_treasures(self, grid, distances, door, start, monsters):
        """Drop treasure chests on free reachable floor tiles."""
        count = settings.TREASURES_BASE + settings.TREASURES_PER_LEVEL * (self.level - 1)
        occupied = {start, door} | {m.pos for m in monsters}
        candidates = [pos for pos in distances
                      if pos not in occupied and distances[pos] >= 2]
        self.rng.shuffle(candidates)
        return [Treasure(x, y) for (x, y) in candidates[:count]]