"""Procedural level generation for the 80x80 tower grid.
Guarantees at least one valid path from the start position to the door
by carving a perfect maze (recursive backtracker) and then braiding it;
the result is verified with a BFS flood fill before being returned.
"""
def generate_level(level):
    for attempt in range(MAX_GENERATION_ATTEMPTS):
        grid = _carve_maze_grid()
        _braid_maze(grid)
        start = (1,1)
        door = (GRID_WIDTH-2, GRID_HEIGHT-2)
        if _path_exists(grid, start, door):
            monsters = _place_monsters(grid, level, start, door)
            chests = _place_chests(grid, start, door, monsters)
            return LevelMap(grid, start, door, monsters, chests)
    # fallback: fully open grid (guaranteed path)
    ...