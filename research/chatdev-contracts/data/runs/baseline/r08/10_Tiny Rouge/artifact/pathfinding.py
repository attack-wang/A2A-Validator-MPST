'''Breadth-first-search helpers used to guarantee the map is always solvable.'''
import random
from collections import deque
import settings
def bfs_path(grid, start, goal, blocked=None):
    '''Return the shortest walkable path from start to goal as a list of (x, y),
    or None when the goal cannot be reached. `blocked` is an optional set of
    extra impassable cells (used to treat monsters as obstacles).'''
    if start == goal:
        return [start]
    blocked = blocked if blocked is not None else set()
    visited = {start}
    parent = {}
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        if cur == goal:
            path = [cur]
            while cur in parent:
                cur = parent[cur]
                path.append(cur)
            path.reverse()
            return path
        x, y = cur
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nx, ny = x + dx, y + dy
            nxt = (nx, ny)
            if not (0 <= nx < settings.GRID_SIZE and 0 <= ny < settings.GRID_SIZE):
                continue
            if nxt in visited or nxt in blocked:
                continue
            if grid[ny][nx] == settings.WALL:
                continue
            visited.add(nxt)
            parent[nxt] = cur
            queue.append(nxt)
    return None
def reachable_cells(grid, start, blocked=None):
    '''Return the set of cells reachable from start (4-directional movement).'''
    blocked = blocked if blocked is not None else set()
    visited = {start}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nx, ny = x + dx, y + dy
            nxt = (nx, ny)
            if not (0 <= nx < settings.GRID_SIZE and 0 <= ny < settings.GRID_SIZE):
                continue
            if nxt in visited or nxt in blocked:
                continue
            if grid[ny][nx] == settings.WALL:
                continue
            visited.add(nxt)
            queue.append(nxt)
    return visited
def carve_path(grid, start, goal):
    '''Carve an L-shaped corridor of FLOOR tiles between start and goal so the
    map is always solvable even after random wall scattering. Both endpoints
    are forced walkable as well.'''
    sx, sy = start
    gx, gy = goal
    grid[sy][sx] = settings.FLOOR
    grid[gy][gx] = settings.FLOOR
    x, y = sx, sy
    if random.random() < 0.5:      # horizontal first, then vertical
        while x != gx:
            x += 1 if gx > x else -1
            grid[y][x] = settings.FLOOR
        while y != gy:
            y += 1 if gy > y else -1
            grid[y][x] = settings.FLOOR
    else:                          # vertical first, then horizontal
        while y != gy:
            y += 1 if gy > y else -1
            grid[y][x] = settings.FLOOR
        while x != gx:
            x += 1 if gx > x else -1
            grid[y][x] = settings.FLOOR