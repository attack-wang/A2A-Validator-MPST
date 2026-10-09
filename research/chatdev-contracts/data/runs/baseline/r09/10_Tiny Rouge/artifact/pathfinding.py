'''
pathfinding.py
Breadth-first-search utilities used to guarantee that every generated
floor always contains at least one valid route from the start to the door.
'''
from collections import deque
DIRS4 = ((0, -1), (-1, 0), (0, 1), (1, 0))  # up, left, down, right
def bfs_reachable(grid, start, is_passable):
    '''
    Return the set of (x, y) cells reachable from `start` moving through
    tiles for which `is_passable(tile_value)` is True.
    '''
    height = len(grid)
    width = len(grid[0])
    seen = {start}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for dx, dy in DIRS4:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in seen and is_passable(grid[ny][nx]):
                    seen.add((nx, ny))
                    queue.append((nx, ny))
    return seen
def has_path(grid, start, goal, is_passable):
    '''True if a passable route exists between start and goal.'''
    if not is_passable(grid[goal[1]][goal[0]]):
        return False
    return goal in bfs_reachable(grid, start, is_passable)
def find_path(grid, start, goal, is_passable):
    '''
    Return a list of (x, y) cells from start to goal (both inclusive),
    or None when no route exists.
    '''
    if not is_passable(grid[goal[1]][goal[0]]):
        return None
    height = len(grid)
    width = len(grid[0])
    prev = {start: None}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            break
        for dx, dy in DIRS4:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in prev and is_passable(grid[ny][nx]):
                    prev[(nx, ny)] = (x, y)
                    queue.append((nx, ny))
    if goal not in prev:
        return None
    path = []
    cell = goal
    while cell is not None:
        path.append(cell)
        cell = prev[cell]
    path.reverse()
    return path