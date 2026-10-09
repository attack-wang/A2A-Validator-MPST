class StrandsGame:
    """Controller: builds grids, verifies merges, runs the command loop."""
    MAX_BUILD_ATTEMPTS = 80
    PATH_CAP = 160
    def __init__(self, puzzles=None, seed=None):
        self._rng = random.Random(seed)
        self._puzzle_bank = puzzles or PUZZLE_BANK
        self.grid = None
        self.puzzle = None
        self._current_index = None
        self.hints_used = 0
        self.complete = False