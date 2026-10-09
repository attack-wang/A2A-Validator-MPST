class MapGenerator:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
    def generate(self, level_number):
        grid = self._carve_maze()
        self._braid_dead_ends(grid)
        self._carve_rooms(grid)
        start = (1, 1)
        door = (settings.GRID_WIDTH - 2, settings.GRID_HEIGHT - 2)  # (78,78)
        # ensure door tile is floor
        grid[door_y][door_x] = FLOOR
        if not self._path_exists(grid, start, door):
            # extremely unlikely; regenerate
            return self.generate(level_number)
        monsters, chests = self._populate(grid, level_number, start, door)
        return Level(...)